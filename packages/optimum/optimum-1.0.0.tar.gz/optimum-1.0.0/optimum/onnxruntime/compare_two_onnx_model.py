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

import copy
import os
from collections import OrderedDict
from pathlib import Path
from typing import Callable, Optional, Union

import numpy as np
from transformers import AutoTokenizer, PretrainedConfig
from transformers.onnx import export
from transformers.onnx.features import FeaturesManager
from transformers.utils import logging

import onnx
from onnx import load_model
from onnxruntime.transformers.onnx_model_bert import BertOnnxModel
from onnxruntime.transformers.optimizer import FusionOptions, get_fusion_statistics, optimize_model
from optimum.onnxruntime.configuration import ORTConfig
from optimum.onnxruntime.utils import generate_identified_filename


logger = logging.get_logger(__name__)


import onnx
from onnx import numpy_helper


# onnx_model_1_path = "/tmp/static_no_add_quantized/model-quantized.onnx"
# onnx_model_1_path = "/tmp/static_bert_all_op_type/model-quantized.onnx"
# onnx_model_1_path = "/tmp/static_bert_all_min_type/model-quantized.onnx"

onnx_model_1_path = "/tmp/distilbert/all_but_not_add/model-quantized.onnx"
onnx_model_1 = onnx.load(onnx_model_1_path)
INTIALIZERS = onnx_model_1.graph.initializer
onnx_weights_1 = {}
for initializer in INTIALIZERS:
    W = numpy_helper.to_array(initializer)
    onnx_weights_1[initializer.name] = W


# onnx_model_2_path = "/tmp/static_reduce/model-quantized.onnx"
# onnx_model_2_path = "/tmp/static_bert_all_min_type_reduce_1/model-quantized.onnx"
onnx_model_2_path = "/tmp/distilbert/restricted_no_transpose/model-quantized.onnx"

onnx_model_2 = onnx.load(onnx_model_2_path)
INTIALIZERS = onnx_model_2.graph.initializer
onnx_weights_2 = {}
for initializer in INTIALIZERS:
    W = numpy_helper.to_array(initializer)
    onnx_weights_2[initializer.name] = W


if onnx_weights_1.keys() != onnx_weights_2.keys():
    print("The keys are not the same !!!!")
    import pdb

    pdb.set_trace()
    x = set(onnx_weights_1.keys())
    y = set(onnx_weights_2.keys())
    print("x-y :", x - y)
    print("y-x :", y - x)

for key, value in onnx_weights_1.items():
    if isinstance(onnx_weights_1[key], np.ndarray):
        if not (onnx_weights_1[key] == onnx_weights_2[key]).all():
            import pdb

            pdb.set_trace()
    else:
        if onnx_weights_1[key] != onnx_weights_2[key]:
            import pdb

            pdb.set_trace()
        # print(onnx_weights_1[key] == onnx_weights_2[key])
    print(key)
    # import pdb;pdb.set_trace()
