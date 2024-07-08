# Import necessary libraries
import pygame
from pygame.locals import *
from random import choice  # Import choice function

# Initialize Pygame
pygame.init()
pygame.font.init()

# Constants
WIDTH, HEIGHT = 750, 500
CAPTION = '2048'

TOP, LEFT = 125, 50
BLOCK_WIDTH, BLOCK_HEIGHT = 75, 75
GAP = 7

MAIN_MENU_FONT = pygame.font.SysFont('Tahoma', 45)
TITLE_FONT = pygame.font.SysFont('Tahoma', 75)
BLOCK_FONT = pygame.font.SysFont('Tahoma', 25)
STATS_FONT = pygame.font.SysFont('Tahoma', 40)
GAME_OVER_FONT = pygame.font.SysFont('Tahoma', 45)

# Credit for Colors - https://github.com/yangshun/2048-python/blob/master/constants.py
BLACK = '#000000'
WHITE = '#ffffff'
BLUE =  '#0000ff'
RED =   '#ff0000'

BG_COLOR = '#bbada0'

COLOR_MAP = {
    0:     ('#CCC0B4', None),
    2:     ('#eee4da', '#776e65'),
    4:     ('#ede0c8', '#776e65'),
    8:     ('#f2b179', '#f9f6f2'),
    16:    ('#f59563', '#f9f6f2'),
    32:    ('#f67c5f', '#f9f6f2'),
    64:    ('#f65e3b', '#f9f6f2'),
    128:   ('#edcf72', '#f9f6f2'),
    256:   ('#edcc61', '#f9f6f2'),
    512:   ('#edc850', '#f9f6f2'),
    1024:  ('#edc53f', '#f9f6f2'),
    2048:  ('#edc22e', '#f9f6f2'),
    4096:  ('#eee4da', '#776e65'),
    8192:  ('#edc22e', '#f9f6f2'),
    16384: ('#f2b179', '#776e65'),
    32768: ('#f59563', '#776e65'),
    65536: ('#f67c5f', '#f9f6f2')
}

# App class for the 2048 game
class App_2048:
    def __init__(self, end=None):
        self.end = end
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(CAPTION)

    def init_variables(self):
        self.running = True
        self.score = 0
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.add_block()

    def exit(self):
        pygame.quit()
        quit()

    def rot90(self, matrix):
        return [list(reversed(row)) for row in zip(*matrix)]

    def rot180(self, matrix):
        return self.rot90(self.rot90(matrix))

    def rot270(self, matrix):
        return self.rot180(self.rot90(matrix))

    def push_right(self):
        for col in range(len(self.grid[0]) - 2, -1, -1):
            for row in self.grid:
                if row[col + 1] == 0:
                    row[col], row[col + 1] = 0, row[col]
                elif row[col + 1] == row[col]:
                    self.score += row[col] * 2
                    row[col], row[col + 1] = 0, row[col] * 2

    def right(self):
        self.push_right()
        self.update()

    def left(self):
        self.grid = self.rot180(self.grid)
        self.push_right()
        self.grid = self.rot180(self.grid)
        self.update()

    def up(self):
        self.grid = self.rot90(self.grid)
        self.right()
        self.grid = self.rot270(self.grid)
        self.update()

    def down(self):
        self.grid = self.rot270(self.grid)
        self.push_right()
        self.grid = self.rot90(self.grid)
        self.update()

    def game_state(self):
        if self.end:
            for row in range(len(self.grid)):
                for col in range(len(self.grid[row])):
                    if self.grid[row][col] == self.end:
                        return 'WIN'

        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == 0:
                    return 'BLOCK AVAILABLE'

        for row in range(len(self.grid)):
            for col in range(len(self.grid[row]) - 1):
                if self.grid[row][col] == self.grid[row][col + 1]:
                    return 'CAN MERGE'

        for row in range(len(self.grid) - 1):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == self.grid[row + 1][col]:
                    return 'CAN MERGE'

        return 'LOSE'

    def add_block(self):
        free_blocks = [(y, x) for y, row in enumerate(self.grid) for x, num in enumerate(row) if num == 0]
        if free_blocks:
            y, x = choice(free_blocks)
            self.grid[y][x] = 2

    def update(self):
        state = self.game_state()
        if state == 'WIN':
            self.game_over(True)
        elif state == 'LOSE':
            self.game_over(False)
        elif state == 'BLOCK AVAILABLE':
            self.add_block()

    def game_over(self, win):
        self.draw_win()
        if win:
            label = GAME_OVER_FONT.render(f'You won! You scored {self.score} points.', 1, BLUE)
        else:
            label = GAME_OVER_FONT.render(f'You lost! You scored {self.score} points.', 1, RED)
        self.win.blit(label, (WIDTH//2 - label.get_width()//2, HEIGHT//2 - label.get_height()//2))
        pygame.display.update()
        pygame.time.delay(3000)
        self.running = False

    def draw_win(self):
        self.win.fill(BLACK)
        self.draw_grid()
        self.draw_stats()

    def draw_grid(self):
        pygame.draw.rect(self.win, BG_COLOR, (LEFT - GAP, TOP - GAP, len(self.grid[0]) * (BLOCK_WIDTH + GAP) + GAP, len(self.grid) * (BLOCK_HEIGHT + GAP) + GAP))
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                x = LEFT + (col * (BLOCK_WIDTH + GAP))
                y = TOP + (row * (BLOCK_HEIGHT + GAP))
                value = self.grid[row][col]
                bg_color, font_color = COLOR_MAP[value]
                color_rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)
                pygame.draw.rect(self.win, bg_color, color_rect)

                if value != 0:
                    label = BLOCK_FONT.render(str(value), 1, font_color)
                    font_rect = label.get_rect()
                    font_rect.center = color_rect.center
                    self.win.blit(label, font_rect)

    def draw_stats(self):
        label = TITLE_FONT.render(f'2048', 1, WHITE)
        self.win.blit(label, (150, 5))

        label = STATS_FONT.render(f'Score: {self.score}', 1, WHITE)
        self.win.blit(label, (400, 125))

    def main(self):
        self.init_variables()
        while self.running:
            self.draw_win()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()
                if event.type == KEYDOWN:
                    if event.key in [K_a, K_LEFT]:
                        self.left()
                    if event.key in [K_d, K_RIGHT]:
                        self.right()
                    if event.key in [K_w, K_UP]:
                        self.up()
                    if event.key in [K_s, K_DOWN]:
                        self.down()
        self.main_menu()

    def main_menu(self):
        self.win.fill(BLACK)
        label = MAIN_MENU_FONT.render('Press any key to start...', 1, WHITE)
        self.win.blit(label, (WIDTH//2 - label.get_width()//2, HEIGHT//2 - label.get_height()//2))
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.exit()
                if event.type in [KEYDOWN, MOUSEBUTTONDOWN]:
                    running = False
        self.main()

if __name__ == '__main__':
    app = App_2048()
    app.main_menu()

    # Quit Pygame
pygame.quit()
