# importing libraries
import pygame
import random

game_name = 'Snake Game @ Python'
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# reset func

class SnakeGameState:

    def __init__(self):
        # define constants
        self.snake_speed = 15
        self.window_x = 720
        self.window_y = 480
        self.fruit_spawn = True
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.snake_body = [[100, 50],
                           [90, 50],
                           [80, 50],
                           [70, 50]]
        self.score = 0
        self.snake_position = [100, 50]
        self.fruit_position = [random.randrange(1, (self.window_x // 10)) * 10,
                               random.randrange(1, (self.window_y // 10)) * 10]
        self.game_over = False

    def update_snake_position(self, snake_position):
        self.snake_position = snake_position
        return self

    def update_fruit_position(self, fruit_position):
        self.fruit_position = fruit_position
        return self

    def update_score(self, score):
        self.score = score
        return self

    def update_direction(self, direction):
        self.direction = direction
        return self

    def game_over(self):
        self.game_over = True
        return self

    def __str__(self):
        return "SnakeGameState: snake_position=" + str(self.snake_position) + ", fruit_position=" \
               + str(self.fruit_position) + ", score=" + str(self.score) + ", direction=" + str(self.direction)


class SnakeGame:
    def __init__(self):
        self.game_state = SnakeGameState()
        self.reward = 0

        # Initialising pygame
        pygame.init()
        # Initialise game window
        pygame.display.set_caption(game_name)
        self.game_window = pygame.display.set_mode((self.game_state.window_x, self.game_state.window_y))
        # FPS (frames per second) controller
        self.fps = pygame.time.Clock()

    def reset(self):
        self.game_state = SnakeGameState()

    def show_score(self, color, font, size):
        # creating font object score_font
        score_font = pygame.font.SysFont(font, size)

        # create the display surface object
        # score_surface
        score_surface = score_font.render('score : ' + str(self.game_state.score), True, color)

        # create a rectangular object for the text
        # surface object
        score_rect = score_surface.get_rect()

        # displaying text
        self.game_window.blit(score_surface, score_rect)
        
    def game_over(self):
        # creating font object my_font
        my_font = pygame.font.SysFont('times new roman', 50)

        # creating a text surface on which text
        # will be drawn
        game_over_surface = my_font.render(
            'Your self.score is : ' + str(self.game_state.score), True, red)

        # create a rectangular object for the text
        # surface object
        game_over_rect = game_over_surface.get_rect()

        # setting position of the text
        game_over_rect.midtop = (self.game_state.window_x / 2, self.game_state.window_y / 4)

        # blit will draw the text on screen
        self.game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()

        # after 2 seconds we will quit the program
        # time.sleep(2)

        # deactivating pygame library
        pygame.quit()

        # self.run_game()

    def play_step(self):
        while True:
            # handling key events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.game_state.change_to = 'UP'
                    if event.key == pygame.K_DOWN:
                        self.game_state.change_to = 'DOWN'
                    if event.key == pygame.K_LEFT:
                        self.game_state.change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT:
                        self.game_state.change_to = 'RIGHT'
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

            # If two keys pressed simultaneously
            # we don't want snake to move into two
            # directions simultaneously
            if self.game_state.change_to == 'UP' and self.game_state.direction != 'DOWN':
                self.game_state.update_direction('UP')
            if self.game_state.change_to == 'DOWN' and self.game_state.direction != 'UP':
                self.game_state.update_direction('DOWN')
            if self.game_state.change_to == 'LEFT' and self.game_state.direction != 'RIGHT':
                self.game_state.update_direction('LEFT')
            if self.game_state.change_to == 'RIGHT' and self.game_state.direction != 'LEFT':
                self.game_state.update_direction('RIGHT')

            # Moving the snake
            if self.game_state.direction == 'UP':
                self.game_state.snake_position[1] -= 10
            if self.game_state.direction == 'DOWN':
                self.game_state.snake_position[1] += 10
            if self.game_state.direction == 'LEFT':
                self.game_state.snake_position[0] -= 10
            if self.game_state.direction == 'RIGHT':
                self.game_state.snake_position[0] += 10

            self.game_state.update_snake_position(self.game_state.snake_position)

            # Snake body growing mechanism
            # if fruits and snakes collide then scores
            # will be incremented by 10
            self.game_state.snake_body.insert(0, list(self.game_state.snake_position))
            if self.game_state.snake_position[0] == self.game_state.fruit_position[0] \
                    and self.game_state.snake_position[1] == self.game_state.fruit_position[1]:
                self.game_state.score += 10
                self.game_state.update_score(self.game_state.score)
                self.game_state.fruit_spawn = False
            else:
                self.game_state.snake_body.pop()

            if not self.game_state.fruit_spawn:
                self.game_state.fruit_position = [random.randrange(1, (self.game_state.window_x // 10)) * 10,
                                                  random.randrange(1, (self.game_state.window_y // 10)) * 10]

            self.game_state.fruit_spawn = True
            self.game_state.update_fruit_position(self.game_state.fruit_position)
            self.game_window.fill(black)

            for pos in self.game_state.snake_body:
                pygame.draw.rect(self.game_window, green,
                                 pygame.Rect(pos[0], pos[1], 10, 10))
                pygame.draw.rect(self.game_window, white, pygame.Rect(
                                 self.game_state.fruit_position[0], self.game_state.fruit_position[1], 10, 10))

            # Game Over conditions
            if self.game_state.snake_position[0] < 0 \
                    or self.game_state.snake_position[0] > self.game_state.window_x - 10:
                self.game_over()

            if self.game_state.snake_position[1] < 0 \
                    or self.game_state.snake_position[1] > self.game_state.window_y - 10:
                self.game_over()

            # Touching the snake body
            for block in self.game_state.snake_body[1:]:
                if self.game_state.snake_position[0] == block[0] and self.game_state.snake_position[1] == block[1]:
                    self.game_over()

            # displaying score continuously
            self.show_score(white, 'times new roman', 20)

            # Refresh game screen
            pygame.display.update()

            # Frame Per Second /Refresh Rate
            self.fps.tick(self.game_state.snake_speed)

    def run(self):
        self.__init__()
        self.play_step()
