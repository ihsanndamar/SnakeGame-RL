import random
import numpy as np
from collections import deque
from keras.models import Model, load_model
from SnakeGame import SnakeGame
from NeuralNetworkModel import NeuralNetworkModel


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class DQNAgent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()

        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, game):
        game_state = game.game_state
        state = [
            game_state.snake_position[0] / game_state.window_x, game_state.snake_position[1] / game_state.window_y,
            game_state.fruit_position[0] / game_state.window_x, game_state.fruit_position[1] / game_state.window_y,

            game_state.direction == 'RIGHT',
            game_state.direction == 'LEFT',
            game_state.direction == 'UP',
            game_state.direction == 'DOWN',

            game_state.is_game_over,

            game_state.snake_body[0][0] / game_state.window_x, game_state.snake_body[0][1] / game_state.window_y,
            game_state.snake_body[1][0] / game_state.window_x, game_state.snake_body[1][1] / game_state.window_y,
            game_state.snake_body[2][0] / game_state.window_x, game_state.snake_body[2][1] / game_state.window_y,
            game_state.snake_body[3][0] / game_state.window_x, game_state.snake_body[3][1] / game_state.window_y,

            game_state.fruit_spawn,

            game_state.score
        ]
        return np.array(state, dtype=np.float32)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        pass

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            model = NeuralNetworkModel(input_shape=(19,), action_space=4).model
            move = np.argmax(model.predict(state.reshape(1, -1)))
            if 0 <= move < 3:
                final_move[move] = 1

        return final_move


def train():
    total_score = 0
    record = 0
    agent = DQNAgent()
    game = SnakeGame()

    while True:
        state_old = agent.get_state(game)

        action = agent.get_action(state_old)

        reward, done, score = game.play_step(action)

        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, action, reward, state_new, done)

        agent.remember(state_old, action, reward, state_new, done)


if __name__ == "__main__":
    train()
