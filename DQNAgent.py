import random
import time

import numpy as np
from collections import deque

import pygame
from keras.models import Model, load_model
from SnakeGame import SnakeGame
from NeuralNetworkModel import NeuralNetworkModel


MAX_MEMORY = 100_000
BATCH_SIZE = 20
LR = 0.001


class DQNAgent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0.01 # randomness
        self.gamma = 0.3  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()

        self.model = NeuralNetworkModel(input_shape=(15,), action_space=3).model


    def get_state(self, game):
        head = game.game_state.snake_position
        food = game.game_state.fruit_position
        point_l = [head[0] - 10, head[1]]
        point_r = [head[0] + 10, head[1]]
        point_u = [head[0], head[1] - 10]
        point_d = [head[0], head[1] + 10]

        dir_l = game.game_state.direction == 'LEFT'
        dir_r = game.game_state.direction == 'RIGHT'
        dir_u = game.game_state.direction == 'UP'
        dir_d = game.game_state.direction == 'DOWN'

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),
            # Danger right
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),
            # Danger left
            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            # Food location
            food[0] < head[0],  # food left
            food[0] > head[0],  # food right
            food[1] < head[1],  # food up
            food[1] > head[1],  # food down
            # Head direction
            game.game_state.direction == 'LEFT',
            game.game_state.direction == 'RIGHT',
            game.game_state.direction == 'UP',
            game.game_state.direction == 'DOWN',
            # Tail direction
            # tail[0] < head[0],  # tail left
            # tail[0] > head[0],  # tail right
            # tail[1] < head[1],  # tail up
            # tail[1] > head[1]  # tail down
        ]

        return np.array(state, dtype=np.float32)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        # predict according to the model
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.model.predict(np.array(states))


    def train_short_memory(self, state, action, reward, next_state, done):
        self.model.predict(np.array([state]))


    def get_action(self, state):
        self.epsilon = 200
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            move = np.argmax(self.model.predict(np.array([state]))[0])
            if 0 <= move < 3:
                final_move[move] = 1

        return final_move



def train():
    plot_scores = []
    plot_mean_scores = []

    total_score = 0
    record = 0
    agent = DQNAgent()
    game = SnakeGame()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        state_old = agent.get_state(game)

        action = agent.get_action(state_old)
        reward, done, score = game.play_step(action)

        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, action, reward, state_new, done)

        agent.remember(state_old, action, reward, state_new, done)

        if done:
            time.sleep(0.2)
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            if score > record:
                record = score
                # agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)
            plot_scores.append(score)
            total_score += score
            total_score += score

            print('Average Score:', total_score / agent.n_games)
            print('Epsilon:', agent.epsilon)
            print('')



if __name__ == "__main__":
    train()

