#  Copyright 2021 The HuggingFace Team. All rights reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from enum import Enum
from pathlib import Path
from typing import Callable, ClassVar, Dict, List, Optional, Tuple, Union

import numpy
import torch
from datasets import Dataset, load_dataset
from torch.utils.data import DataLoader, RandomSampler
from transformers import AutoTokenizer, default_data_collator
from transformers.onnx import OnnxConfig, export, validate_model_outputs

import onnx
from onnxruntime.quantization import (
    CalibrationDataReader,
    QuantFormat,
    QuantType,
    onnx_model,
    quantize_dynamic,
    quantize_static,
)
from onnxruntime.quantization.calibrate import CalibrationDataReader, CalibrationMethod
from optimum.onnxruntime.utils import generate_identified_filename


class ORTQuantizationMode(Enum):

    DYNAMIC = "dynamic"
    STATIC = "static"


SUPPORTED_QUANT_MODE = set([approach.value for approach in ORTQuantizationMode])


class ORTQuantizer:
    def __init__(
        self,
        model_name_or_path,
        output_dir,
        quantization_approach=None,
        per_channel=False,
        reduce_range=False,
        activation_type=QuantType.QUInt8,
        weight_type=QuantType.QUInt8,
        optimize_model=True,
        quant_format=QuantFormat.QOperator,
        calibrate_method=CalibrationMethod.MinMax,
        use_external_data_format=False,
        calib_dataset=None,
        dataset_name=None,
        dataset_config_name=None,
        data_files=None,
        preprocess_function=None,
        batch_size=8,
        split="train",
        max_samples=None,
        cache_dir=None,
        config=None,
    ):
        self.model_name_or_path = model_name_or_path
        self.output_dir = output_dir if isinstance(output_dir, Path) else Path(output_dir)
        self.model_path = self.output_dir.joinpath("model.onnx")
        self.quant_model_path = generate_identified_filename(self.model_path, "-quantized")

        self.config = config
        self.approach = quantization_approach
        self.per_channel = per_channel
        self.reduce_range = reduce_range
        self.activation_type = activation_type
        self.weight_type = weight_type
        self.optimize_model = optimize_model
        self.use_external_data_format = use_external_data_format

        self.quant_format = quant_format
        self.calibrate_method = calibrate_method

        self.calib_dataset = calib_dataset
        self.dataset_name = dataset_name
        self.dataset_config_name = dataset_config_name
        self.data_files = data_files
        self.preprocess_function = preprocess_function
        self.batch_size = batch_size
        self.split = split
        self.max_samples = max_samples
        self.cache_dir = cache_dir

        self.onnx_config = None
        self.feature = "default"
        self.opset = None

    def export(self):
        """
        Load and export a model to an ONNX Intermediate Representation (IR).
        """
        from transformers.onnx import export, validate_model_outputs
        from transformers.onnx.features import FeaturesManager

        tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path)
        model = FeaturesManager.get_model_from_feature(self.feature, self.model_name_or_path)
        model_type, model_onnx_config = FeaturesManager.check_supported_model_or_raise(model, feature=self.feature)
        self.onnx_config = model_onnx_config(model.config)
        self.opset = self.onnx_config.default_onnx_opset if self.opset is None else self.opset
        onnx_inputs, onnx_outputs = export(tokenizer, model, self.onnx_config, self.opset, self.model_path)

    def fit(self):

        self.export()

        if self.approach == ORTQuantizationMode.DYNAMIC.value:
            quantize_dynamic(
                self.model_path,
                self.quant_model_path,
                per_channel=self.per_channel,
                reduce_range=self.reduce_range,
                activation_type=self.activation_type,
                weight_type=self.weight_type,
                optimize_model=self.optimize_model,
                use_external_data_format=self.use_external_data_format,
            )

        elif self.approach == ORTQuantizationMode.STATIC.value:

            calibration_data_reader = self.create_calibrator()

            quantize_static(
                self.model_path,
                self.quant_model_path,
                calibration_data_reader,
                quant_format=self.quant_format,
                per_channel=self.per_channel,
                reduce_range=self.reduce_range,
                activation_type=self.activation_type,
                weight_type=self.weight_type,
                optimize_model=self.optimize_model,
                use_external_data_format=self.use_external_data_format,
                calibrate_method=self.calibrate_method,
            )

        else:
            raise ValueError(
                "Unknown quantization approach. Supported approach are " + ", ".join(SUPPORTED_QUANT_MODE)
            )

    def create_calibrator(self):

        calibration_data_reader = HFCalibrationDataReader(
            self.onnx_config,
            self.batch_size,
            calib_dataset=self.calib_dataset,
            dataset_name=self.dataset_name,
            dataset_config_name=self.dataset_config_name,
            data_files=self.data_files,
            preprocess_function=self.preprocess_function,
            batch_size=self.batch_size,
            split=self.split,
            max_samples=self.max_samples,
            cache_dir=self.cache_dir,
        )

        return calibration_data_reader


class HFCalibrationDataReader(CalibrationDataReader):
    def __init__(
        self,
        onnx_config: OnnxConfig,
        batch_size: int,
        calib_dataset: Optional[Dataset] = None,
        dataset_name: Optional[str] = None,
        dataset_config_name: Optional[str] = None,
        data_files: Optional[str] = None,
        preprocess_function: Optional[Callable] = None,
        split: Optional[str] = None,
        max_samples: int = None,
        cache_dir: Optional[str] = None,
    ):
        """
        Args:
            onnx_config (:obj:`OnnxConfig`):
                Configuration holding the model's ONNX export properties.
            calib_dataset (:obj:`Dataset`, `optional`):
                Dataset to use for the calibration step.
            dataset_name (:obj:`str`, `optional`):
                Dataset repository name on the Hugging Face Hub or path to a local directory containing data files to
                load to use for the calibration step.
            dataset_config_name (:obj:`str`, `optional`):
                Name of the dataset configuration.
            data_files (:obj:`str`, `optional`):
                Path to source data files.
            preprocess_function (:obj:`Callable`, `optional`):
                Processing function to apply to each example after loading dataset.
            batch_size (:obj:`int`):
                How many samples per batch to load.
            split (:obj:`str`):
                Which split of the data to use for the calibration step.
            max_samples (:obj:`int`)
                Maximum number of samples used for the calibration step.
            cache_dir (:obj:`str`, `optional`):
                Path to a directory in which a downloaded configuration should be cached if the standard cache should
                not be used.
        """

        if calib_dataset is None and (dataset_name is None or preprocess_function is None):
            raise ValueError("Dataset or path to load it must be provided")

        if calib_dataset is None:
            calib_dataset = load_dataset(
                dataset_name,
                name=dataset_config_name,
                data_files=data_files,
                split=split,
                cache_dir=cache_dir,
            )
            calib_dataset = calib_dataset.map(preprocess_function, batched=True)

        if max_samples is not None:
            calib_dataset = calib_dataset.select(range(max_samples))

        ignored_columns = list(set(calib_dataset.column_names) - set(onnx_config.inputs.keys()))
        calib_dataset = calib_dataset.remove_columns(ignored_columns)

        generator = torch.Generator()
        generator.manual_seed(int(torch.empty((), dtype=torch.int64).random_().item()))
        sampler = RandomSampler(calib_dataset, generator=generator)

        calib_dataloader = DataLoader(
            calib_dataset,
            batch_size=batch_size,
            sampler=sampler,
            collate_fn=default_data_collator,
        )
        self._iter = iter([{key: data[key].detach().numpy() for key in data} for data in calib_dataloader])

    def get_next(self):
        return next(self._iter, None)
