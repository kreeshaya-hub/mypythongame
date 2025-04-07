import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Skills Game")

# Set up colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Clock and speed
clock = pygame.time.Clock()
snake_speed = 12

# Snake starting position
snake_pos = [100, 50]
snake_body = [[100, 50]]

# Movement direction
direction = 'RIGHT'

# Snake size
BLOCK_SIZE = 20

def draw_snake(snake_body):
    for block in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movement
    if direction == 'RIGHT':
        snake_pos[0] += BLOCK_SIZE
    elif direction == 'LEFT':
        snake_pos[0] -= BLOCK_SIZE
    elif direction == 'UP':
        snake_pos[1] -= BLOCK_SIZE
    elif direction == 'DOWN':
        snake_pos[1] += BLOCK_SIZE

    # Update snake body
    snake_body.insert(0, list(snake_pos))
    snake_body.pop()

    # Draw everything
    screen.fill(BLACK)
    draw_snake(snake_body)
    pygame.display.update()

    # Control the game speed
    clock.tick(snake_speed)
