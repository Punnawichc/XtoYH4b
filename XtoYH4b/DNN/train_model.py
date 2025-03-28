#######################################################

# This script is very simple, just opens the train dataset and performs training.
# The model in this file is DNN implemented using TensorFlow Sequential.

# command to run this scripts:
# python3 train_model.py

# Created by Punnawich Chokeprasert, punnawich.chokeprasert@cern.ch
# 27 Mar 2025

#######################################################

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.optimizers import Adam


df_train = pd.read_csv("train_data.csv")

print(df_train)

x_train, y_train  = df_train.iloc[:, 1:], df_train.iloc[:, 0]

x_train, y_train = x_train.to_numpy(), y_train.to_numpy()

print(f"n_sig for training: {np.sum(y_train == 1)}")
print(f"n_bkg for training: {np.sum(y_train == 0)}")

model = tf.keras.models.Sequential([
tf.keras.layers.Flatten(input_shape=(len(x_train[0]),)),
tf.keras.layers.Dense(128, activation='relu'),
# tf.keras.layers.Dropout(0.2),
tf.keras.layers.Dense(64, activation='relu'),
tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer=Adam(learning_rate=0.001),
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=10, batch_size=32)
# model.evaluate(x_test, y_test)

model.save("model_v2.h5")
