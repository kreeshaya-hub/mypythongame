import pygame
import sys
import random

pygame.init()

# Screen settings
WIDTH, HEIGHT = 1080, 720
BLOCK_SIZE = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Skills Game")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GOLD = (255, 215, 0)

# Game settings
clock = pygame.time.Clock()
snake_speed = 10

# Fonts
font = pygame.font.SysFont('Arial', 24)
big_font = pygame.font.SysFont('Arial', 48)

# Load skill icons
skills = [
    {"name": "Python", "icon": pygame.image.load("icons/Python.png")},
    {"name": "Figma", "icon": pygame.image.load("icons/Figma.png")},
    {"name": "React", "icon": pygame.image.load("icons/React.png")},
    {"name": "JavaScript", "icon": pygame.image.load("icons/JavaScript.png")},
    {"name": "React Native", "icon": pygame.image.load("icons/react-native.png")},  
    {"name": "Adobe CC", "icon": pygame.image.load("icons/adobe-creative-cloud.png")},
    {"name": "Node.js", "icon": pygame.image.load("icons/nodejs.png")},
    {"name": "GitHub", "icon": pygame.image.load("icons/github.png")},
    {"name": "Postman", "icon": pygame.image.load("icons/postman.png")},
    {"name": "MongoDB", "icon": pygame.image.load("icons/mongodb.png")},
]

# Resize icons
for skill in skills:
    skill["icon"] = pygame.transform.scale(skill["icon"], (BLOCK_SIZE, BLOCK_SIZE))


def draw_snake(body):
    for block in body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))


def draw_border():
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), 4)


def show_message(text, color=WHITE):
    msg = font.render(text, True, color)
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT - 30))


def show_game_over():
    while True:
        screen.fill(BLACK)
        draw_border()
        game_over_text = big_font.render("GAME OVER", True, RED)
        retry_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def show_game_won():
    while True:
        screen.fill(BLACK)
        draw_border()
        win_text = big_font.render("YOU FOUND ALL MY SKILLS!", True, GOLD)
        retry_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def main():
    snake_pos = [100, 100]
    snake_body = [list(snake_pos)]
    direction = 'RIGHT'

    remaining_skills = skills.copy()
    current_skill = random.choice(remaining_skills)
    skill_x = random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE)
    skill_y = random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)

    message = ""
    message_timer = 0
    won_timer_started = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'

        # Move snake
        if direction == 'RIGHT':
            snake_pos[0] += BLOCK_SIZE
        elif direction == 'LEFT':
            snake_pos[0] -= BLOCK_SIZE
        elif direction == 'UP':
            snake_pos[1] -= BLOCK_SIZE
        elif direction == 'DOWN':
            snake_pos[1] += BLOCK_SIZE

        # Wall or self collision
        if (snake_pos[0] < 0 or snake_pos[0] >= WIDTH or
            snake_pos[1] < 0 or snake_pos[1] >= HEIGHT or
            snake_pos in snake_body[1:]):
            show_game_over()

        snake_body.insert(0, list(snake_pos))

        # Check collision with skill
        ate_skill = False
        if current_skill:
            snake_rect = pygame.Rect(snake_pos[0], snake_pos[1], BLOCK_SIZE, BLOCK_SIZE)
            icon_rect = pygame.Rect(skill_x, skill_y, BLOCK_SIZE, BLOCK_SIZE)

            if snake_rect.colliderect(icon_rect):
                ate_skill = True
                remaining_skills.remove(current_skill)
                message_timer = pygame.time.get_ticks()

                if not remaining_skills:
                    message = "You collected all skills!"
                    current_skill = None
                    won_timer_started = pygame.time.get_ticks()
                else:
                    message = f"You found {current_skill['name']}! More to go!"
                    current_skill = random.choice(remaining_skills)
                    skill_x = random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE)
                    skill_y = random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)

        if not ate_skill:
            snake_body.pop()

        # Drawing
        screen.fill(BLACK)
        draw_border()
        draw_snake(snake_body)

        # Draw current icon
        if current_skill:
            pygame.draw.rect(screen, WHITE, (skill_x, skill_y, BLOCK_SIZE, BLOCK_SIZE))
            screen.blit(current_skill["icon"], (skill_x, skill_y))

        # Show scoreboard (top-left)
        score = len(skills) - len(remaining_skills)
        score_text = font.render(f"Skills: {score} / {len(skills)}", True, WHITE)
        screen.blit(score_text, (20, 20))

        # Bottom message
        if message and pygame.time.get_ticks() - message_timer < 2000:
            show_message(message)

        pygame.display.update()
        clock.tick(snake_speed)

        if won_timer_started and pygame.time.get_ticks() - won_timer_started > 2000:
            show_game_won()


# Start the game
main()
