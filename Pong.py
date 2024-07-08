import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_SPEED = 5
PADDLE_SPEED = 10
FPS = 60  # Frames per second

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Initialize the clock
clock = pygame.time.Clock()

# Initialize ball position and velocity
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = random.choice((1, -1)) * BALL_SPEED
ball_dy = random.choice((1, -1)) * BALL_SPEED

# Initialize paddles
left_paddle_y = (HEIGHT - 100) // 2
right_paddle_y = (HEIGHT - 100) // 2
paddle_width = 10
paddle_height = 100

# Initialize scores
left_score = 0
right_score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle_y > 0:
        left_paddle_y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle_y < HEIGHT - paddle_height:
        left_paddle_y += PADDLE_SPEED
    if keys[pygame.K_UP] and right_paddle_y > 0:
        right_paddle_y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle_y < HEIGHT - paddle_height:
        right_paddle_y += PADDLE_SPEED

    # Move the ball
    ball_x += ball_dx
    ball_y += ball_dy

    # Collision with top and bottom walls
    if ball_y <= 0 or ball_y >= HEIGHT:
        ball_dy *= -1

    # Collision with paddles
    if (
        ball_x <= 20
        and left_paddle_y <= ball_y <= left_paddle_y + paddle_height
    ) or (
        ball_x >= WIDTH - 20 - paddle_width
        and right_paddle_y <= ball_y <= right_paddle_y + paddle_height
    ):
        ball_dx *= -1

    # Ball out of bounds
    if ball_x < 0:
        # Right player scores a point
        right_score += 1
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_dx = random.choice((1, -1)) * BALL_SPEED
        ball_dy = random.choice((1, -1)) * BALL_SPEED
    elif ball_x > WIDTH:
        # Left player scores a point
        left_score += 1
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_dx = random.choice((1, -1)) * BALL_SPEED
        ball_dy = random.choice((1, -1)) * BALL_SPEED

    # Clear the screen
    screen.fill(BLACK)

    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, (20, left_paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(
        screen, WHITE, (WIDTH - 20 - paddle_width, right_paddle_y, paddle_width, paddle_height)
    )
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), 10)

    # Draw scores
    left_text = font.render(f"Left: {left_score}", True, WHITE)
    right_text = font.render(f"Right: {right_score}", True, WHITE)
    screen.blit(left_text, (50, 20))
    screen.blit(right_text, (WIDTH - 150, 20))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
