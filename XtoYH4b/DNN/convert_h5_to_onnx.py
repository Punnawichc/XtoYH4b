#######################################################

# This scripts is used to convert trained model in .h5 to .onnx.

# command to run this scripts:
# python3 prepare_data.py

# Created by Punnawich Chokeprasert, punnawich.chokeprasert@cern.ch
# 27 Mar 2025

#######################################################

import tensorflow as tf
import tf2onnx
import numpy as np

model = tf.keras.models.load_model("model_v2.h5")
spec = (tf.TensorSpec((None, model.input_shape[1]), tf.float32, name="input"),)

onnx_model, _ = tf2onnx.convert.from_keras(model, input_signature=spec, opset=13)

with open("model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())
