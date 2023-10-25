import random
import numpy as np
from collections import deque
from keras.models import Model, load_model
from SnakeGame import SnakeGame
from NeuralNetworkModel import NeuralNetworkModel

import os

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


class DQNAgent:
    def __init__(self):
        pass

    def get_state(self, game):
        pass

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def get_action(self, state):
        pass


def train():
    pass


if __name__ == "__main__":
    train()
