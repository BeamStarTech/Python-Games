import pygame
import random
import sys

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_SIZE = 30
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
GRAVITY = 0.5
JUMP_HEIGHT = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.speed = 5
        self.is_jumping = False
        self.is_falling = False
        self.movey = 0
        self.gravity = GRAVITY
        self.jumps_left = 2

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and not self.is_jumping and self.jumps_left > 0:
            self.is_jumping = True
            self.is_falling = False
            self.movey = -JUMP_HEIGHT
            self.jumps_left -= 1

        if self.is_jumping:
            self.rect.y += self.movey
            self.movey += self.gravity
            if self.movey > 0:
                self.is_jumping = False
                self.is_falling = True

        if self.is_falling:
            self.rect.y += self.movey
            self.movey += self.gravity
            if self.rect.bottom >= SCREEN_HEIGHT - 20:
                self.rect.bottom = SCREEN_HEIGHT - 20
                self.is_falling = False
                self.movey = 0
                self.jumps_left = 2

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Functions
def generate_platforms(num_platforms):
    platforms = pygame.sprite.Group()
    for i in range(num_platforms):
        if random.random() < 0.2:  # 20% chance of generating a red platform
            platform = Platform(random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH), random.randint(0, SCREEN_HEIGHT - PLATFORM_HEIGHT), PLATFORM_WIDTH, PLATFORM_HEIGHT, RED)
        else:
            platform = Platform(random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH), random.randint(0, SCREEN_HEIGHT - PLATFORM_HEIGHT), PLATFORM_WIDTH, PLATFORM_HEIGHT, WHITE)
        platforms.add(platform)
    return platforms

def check_collision(player, platforms):
    plat_hit_list = pygame.sprite.spritecollide(player, platforms, False)
    for p in plat_hit_list:
        if p.image.get_at((0, 0)) == RED:  # Check if the platform is red
            reset_player(player)
            return -1  # Return -1 to indicate a red platform collision
        else:
            if player.movey > 0:
                player.rect.bottom = p.rect.top
                player.is_falling = False
                player.movey = 0
                player.jumps_left = 2
            break
    else:
        player.is_falling = True
    return 0  # Return 0 to indicate no red platform collision

def reset_player(player):
    player.rect.centerx = SCREEN_WIDTH / 2
    player.rect.bottom = SCREEN_HEIGHT - 20
    player.is_jumping = False
    player.is_falling = False
    player.movey = 0
    player.jumps_left = 2

def display_score(score):
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), 1, WHITE)
    screen.blit(text, (10, 10))

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set title of the window
pygame.display.set_caption("Randomizing Platformer")

# Create the player and platforms
player = Player()
plat_list = generate_platforms(10)
floor = Platform(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20, WHITE)
plat_list.add(floor)

# Initialize score
score = 0

# Show controls popup
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()
messagebox.showinfo("Controls", "Use the left and right arrow keys to move, the space bar to jump, and the 'R' key to reshuffle the platforms.")

# Game loop
while True:
    try:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    plat_list.remove(floor)
                    plat_list.empty()
                    plat_list = generate_platforms(10)
                    plat_list.add(floor)

        # Update the player
        player.update()

        # Check if the player has reached the top of the screen
        if player.rect.top <= 0:
            score += 1
            player.rect.bottom = SCREEN_HEIGHT - 20
            plat_list.remove(floor)
            plat_list.empty()
            plat_list = generate_platforms(10)
            plat_list.add(floor)

        # Check for collision with platforms
        collision_result = check_collision(player, plat_list)
        if collision_result == -1:
            score -= 1
            reset_player(player)

        # Draw everything
        screen.fill(BLACK)
        screen.blit(player.image, player.rect)
        plat_list.draw(screen)
        display_score(score)
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(60)

    except Exception as e:
        print(e)
        pygame.quit()
        sys.exit()
