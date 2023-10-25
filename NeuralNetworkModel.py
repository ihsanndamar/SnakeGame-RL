import os

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import random
import numpy as np
from collections import deque
from keras.models import Model, load_model
from keras.layers import Input, Dense
from keras.optimizers import RMSprop





class NeuralNetworkModel:

    def __init__(self, input_shape, action_space):
        self.model = self.Create(input_shape, action_space)



    def Create(self, input_shape, action_space):
        X_input = Input(input_shape)

        # 'Dense' is the basic form of a neural network layer
        # Input Layer of state size(4) and Hidden Layer with 512 nodes
        X = Dense(512, input_shape=input_shape, activation="relu", kernel_initializer='he_uniform')(X_input)

        # Hidden layer with 256 nodes
        X = Dense(256, activation="relu", kernel_initializer='he_uniform')(X)

        # Hidden layer with 64 nodes
        X = Dense(64, activation="relu", kernel_initializer='he_uniform')(X)

        # Output Layer with # of actions: 2 nodes (left, right)
        X = Dense(action_space, activation="linear", kernel_initializer='he_uniform')(X)

        model = Model(inputs=X_input, outputs=X, name='CartPole DQN model')
        model.compile(loss="mse", optimizer=RMSprop(lr=0.00025, rho=0.95, epsilon=0.01), metrics=["accuracy"])

        model.summary()
        return model

