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

import logging
from enum import Enum
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union

import numpy
import torch
from datasets import Dataset, load_dataset
from torch.utils.data import DataLoader, RandomSampler
from transformers import AutoTokenizer, default_data_collator
from transformers.onnx import OnnxConfig, export, validate_model_outputs
from transformers.onnx.features import FeaturesManager

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
from onnxruntime.transformers.optimizer import FusionOptions, optimize_model
from optimum.onnxruntime.utils import generate_identified_filename


logger = logging.getLogger(__name__)


class ORTQuantizationMode(Enum):

    DYNAMIC = "dynamic"
    STATIC = "static"


SUPPORTED_QUANT_MODE = set([approach.value for approach in ORTQuantizationMode])


calibration_method = {"minmax": CalibrationMethod.MinMax, "entropy": CalibrationMethod.Entropy}

quant_format = {"operator": QuantFormat.QOperator, "qdq": QuantFormat.QDQ}

quant_type = {"int8": QuantType.QInt8, "uint8": QuantType.QUInt8}


class ORTCalibrationDataReader(CalibrationDataReader):
    def __init__(self, calib_dataloader: DataLoader):
        self._iter = iter([{key: data[key].numpy() for key in data} for data in calib_dataloader])

    def get_next(self):
        return next(self._iter, None)


class ORTQuantizer:
    def __init__(
        self,
        model_name_or_path,
        output_dir,
        ort_config,
        feature="default",
        calib_dataset=None,
        dataset_name=None,
        dataset_config_name=None,
        data_files=None,
        preprocess_function=None,
        cache_dir=None,
        optimization_options: Optional[FusionOptions] = None,
    ):
        self.model_name_or_path = model_name_or_path
        self.output_dir = output_dir if isinstance(output_dir, Path) else Path(output_dir)
        self.model_path = self.output_dir.joinpath("model.onnx")
        self.optim_model_path = generate_identified_filename(self.model_path, "-optimized")
        self.quant_model_path = generate_identified_filename(self.model_path, "-quantized")
        self.ort_config = ort_config
        self.optimization_options = optimization_options

        self.quantization_approach = ort_config.quantization_approach
        self.activation_type = quant_type.get(ort_config.activation_type, QuantType.QUInt8)
        self.weight_type = quant_type.get(ort_config.weight_type, QuantType.QUInt8)
        self.quant_format = quant_format.get(ort_config.quant_format, QuantFormat.QOperator)
        self.calibrate_method = calibration_method.get(ort_config.calibration_method, CalibrationMethod.MinMax)

        self.calib_dataset = calib_dataset
        self.dataset_name = dataset_name
        self.dataset_config_name = dataset_config_name
        self.data_files = data_files
        self.preprocess_function = preprocess_function
        self.cache_dir = cache_dir
        self.onnx_config = None

        self.feature = feature
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path)
        self.model = FeaturesManager.get_model_from_feature(self.feature, self.model_name_or_path)

    def export(self):
        """
        Load and export a model to an ONNX Intermediate Representation (IR).
        """
        model_type, model_onnx_config = FeaturesManager.check_supported_model_or_raise(
            self.model, feature=self.feature
        )
        self.onnx_config = model_onnx_config(self.model.config)
        opset = self.onnx_config.default_onnx_opset if self.ort_config.opset is None else self.ort_config.opset
        onnx_inputs, onnx_outputs = export(self.tokenizer, self.model, self.onnx_config, opset, self.model_path)

    def optimize(self):
        """
        Load, optimize and export the ONNX IR
        """
        config = self.model.config
        config_names = {
            "bert": ("num_attention_heads", "hidden_size"),
            "distilbert": ("n_heads", "dim"),
            "roberta": ("num_attention_heads", "hidden_size"),
            "bart": ("encoder_attention_heads", "d_model"),
            "gpt2": ("n_head", "n_embd"),
        }
        model_type = getattr(config, "model_type")
        has_attn = model_type in config_names
        num_heads = getattr(config, config_names[model_type][0]) if has_attn else 0
        hidden_size = getattr(config, config_names[model_type][1]) if has_attn else 0
        model_type = "bert" if "bert" in config.model_type else config.model_type

        optimizer = optimize_model(
            self.model_path.as_posix(),
            model_type,
            num_heads,
            hidden_size,
            opt_level=self.ort_config.opt_level,
            optimization_options=self.optimization_options,
            use_gpu=self.ort_config.use_gpu,
            only_onnxruntime=self.ort_config.only_onnxruntime,
        )

        optimizer.save_model_to_file(self.optim_model_path.as_posix(), self.ort_config.use_external_data_format)

        if optimizer.is_fully_optimized():
            msg = "The model has been fully optimized"
        else:
            msg = "The model has been optimized"

        logger.info(msg + f" and saved at {self.optim_model_path}")

    def fit(self):
        self.export()

        if self.ort_config.optimize_model:
            self.optimize()
            self.model_path = self.optim_model_path

        if self.quantization_approach == ORTQuantizationMode.DYNAMIC.value:
            quantize_dynamic(
                self.model_path,
                self.quant_model_path,
                per_channel=self.ort_config.per_channel,
                reduce_range=self.ort_config.reduce_range,
                activation_type=self.activation_type,
                weight_type=self.weight_type,
                optimize_model=self.ort_config.optimize_model,
                use_external_data_format=self.ort_config.use_external_data_format,
            )

        elif self.quantization_approach == ORTQuantizationMode.STATIC.value:
            calib_dataset = self.calib_dataset if self.calib_dataset is not None else self.get_calib_dataset()
            calib_dataloader = self.get_calib_dataloader(calib_dataset)
            calib_data_reader = self.get_data_reader(calib_dataloader)

            quantize_static(
                self.model_path,
                self.quant_model_path,
                calib_data_reader,
                quant_format=self.quant_format,
                per_channel=self.ort_config.per_channel,
                reduce_range=self.ort_config.reduce_range,
                activation_type=self.activation_type,
                weight_type=self.weight_type,
                optimize_model=self.ort_config.optimize_model,
                use_external_data_format=self.ort_config.use_external_data_format,
                calibrate_method=self.calibrate_method,
            )

        else:
            raise ValueError(
                "Unknown quantization approach. Supported approach are " + ", ".join(SUPPORTED_QUANT_MODE)
            )

    def get_calib_dataset(self) -> Dataset:

        if self.dataset_name is None:
            raise ValueError(
                "ORTQuantizer: static quantization calibration step requires a dataset_name if no calib_dataset is "
                "provided."
            )

        calib_dataset = load_dataset(
            self.dataset_name,
            name=self.dataset_config_name,
            data_files=self.data_files,
            split=self.ort_config.split,
            cache_dir=self.cache_dir,
        )
        calib_dataset = calib_dataset.map(self.preprocess_function, batched=True)

        return calib_dataset

    def get_calib_dataloader(self, calib_dataset: Optional[Dataset] = None) -> DataLoader:

        if calib_dataset is None and self.calib_dataset is None:
            raise ValueError("ORTQuantizer: static quantization calibration step requires a calib_dataset.")

        calib_dataset = calib_dataset if calib_dataset is not None else self.calib_dataset

        if self.ort_config.max_samples is not None and len(calib_dataset) > self.ort_config.max_samples:
            calib_dataset = calib_dataset.select(range(self.ort_config.max_samples))

        ignored_columns = list(set(calib_dataset.column_names) - set(self.onnx_config.inputs.keys()))
        calib_dataset = calib_dataset.remove_columns(ignored_columns)

        generator = torch.Generator()
        generator.manual_seed(int(torch.empty((), dtype=torch.int64).random_().item()))
        sampler = RandomSampler(calib_dataset, generator=generator)

        return DataLoader(
            calib_dataset,
            batch_size=self.ort_config.calib_batch_size,
            sampler=sampler,
            collate_fn=default_data_collator,
        )

    @staticmethod
    def get_data_reader(calib_dataloader: DataLoader) -> ORTCalibrationDataReader:
        return ORTCalibrationDataReader(calib_dataloader)
