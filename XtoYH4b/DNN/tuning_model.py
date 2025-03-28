#######################################################

# This script is very simple, just tuning hyperparameters of Tensorflow Sequential
# and displays result based on the best roc_auc.

# command to run this scripts:
# python3 tuning_model.py

# Created by Punnawich Chokeprasert, punnawich.chokeprasert@cern.ch
# 27 Mar 2025

#######################################################

import pandas as pd
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
# from scikeras.wrappers import KerasClassifier
from sklearn.model_selection import GridSearchCV


def the_model(learning_rate=0.001, neurons=128):
    model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(len(x_train[0]),)),
    tf.keras.layers.Dense(neurons, activation='relu'),
    # tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer=Adam(learning_rate=learning_rate),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    return model

if __name__ == "__main__":

    df_train = pd.read_csv("train_data.csv")
    x_train = df_train.iloc[:, 1:].to_numpy()
    y_train = df_train.iloc[:, 0].to_numpy()

    model = KerasClassifier(build_fn=the_model, epochs=10, batch_size=32, verbose=0)

    param_grid = {
        'learning_rate': [0.0001, 0.001, 0.01], 
        'neurons': [64, 128, 256], 
        'batch_size': [16, 32, 64] 
    }

    grid = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, scoring='roc_auc', n_jobs=4)
    grid_result = grid.fit(x_train, y_train)

    print("Best Parameters:", grid_result.best_params_)
    print("Best Accuracy:", grid_result.best_score_)

    # lastest results (14.03.25)
    # Best Parameters: {'batch_size': 32, 'learning_rate': 0.001, 'neurons': 128}
    # Best Accuracy: 0.6357778722250879  