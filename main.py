import pygame
import sys
import random

pygame.init()

# Screen settings
WIDTH, HEIGHT = 1080, 720
BLOCK_SIZE = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Skills Game")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
YELLOW = (255, 255, 0)
DARK_GREEN = (0, 200, 0)

# Game settings
clock = pygame.time.Clock()
snake_speed = 10
MARGIN_BLOCKS = 2  # margin from the wall (in blocks)

# Fonts
font = pygame.font.SysFont('Arial', 24)
big_font = pygame.font.SysFont('Arial', 48)

# Load skill icons
skills = [
    {"name": "Python", "icon": pygame.image.load("icons/Python.png")},
    {"name": "Figma", "icon": pygame.image.load("icons/Figma.png")},
    {"name": "React", "icon": pygame.image.load("icons/React.png")},
    {"name": "JavaScript", "icon": pygame.image.load("icons/JavaScript.png")},
    {"name": "Wordpress", "icon": pygame.image.load("icons/Wordpress.png")},
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
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), 6)


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


def get_random_position():
    """Generates a random position that isn't too close to the wall."""
    x = random.randrange(MARGIN_BLOCKS, (WIDTH // BLOCK_SIZE) - MARGIN_BLOCKS) * BLOCK_SIZE
    y = random.randrange(MARGIN_BLOCKS, (HEIGHT // BLOCK_SIZE) - MARGIN_BLOCKS) * BLOCK_SIZE
    return x, y


def show_intro_screen():
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)
    button_pressed = False

    while True:
        screen.fill(BLACK)
        draw_border()

        title_text = big_font.render("Hi, This is my Snake Game!", True, GOLD)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        instructions = [
            "1. Use arrow keys on your keyboard to go in that direction.",
            "2. Catch as many skills as you can to learn more about me.",
            "3. Be careful of dashing into the wall or yourself! 😂",
            "4. Enjoy my Game!!"
        ]

        for i, line in enumerate(instructions):
            instr_text = font.render(line, True, WHITE)
            screen.blit(instr_text, (WIDTH // 2 - instr_text.get_width() // 2, HEIGHT // 3 + i * 30))

        # Button color changes on click
        button_color = DARK_GREEN if button_pressed else GREEN
        pygame.draw.rect(screen, button_color, button_rect)
        button_text = font.render("Start Game", True, BLACK)
        screen.blit(button_text, (
            button_rect.centerx - button_text.get_width() // 2,
            button_rect.centery - button_text.get_height() // 2
        ))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    button_pressed = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if button_rect.collidepoint(event.pos) and button_pressed:
                    return  # Start the game
                button_pressed = False


def main():
    snake_pos = [100, 100]
    snake_body = [list(snake_pos)]
    direction = 'RIGHT'

    remaining_skills = skills.copy()
    current_skill = random.choice(remaining_skills)
    skill_x, skill_y = get_random_position()

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
                    message = f"You found {current_skill['name']}!"
                    current_skill = random.choice(remaining_skills)
                    skill_x, skill_y = get_random_position()

        if not ate_skill:
            snake_body.pop()

        # Drawing
        screen.fill(BLACK)
        draw_border()
        draw_snake(snake_body)

        # Draw current icon
        if current_skill:
            # pygame.draw.rect(screen, WHITE, (skill_x, skill_y, BLOCK_SIZE, BLOCK_SIZE))
            screen.blit(current_skill["icon"], (skill_x, skill_y))

        # Draw scoreboard
        score = len(skills) - len(remaining_skills)
        score_surface = font.render(f"Skills: {score} / {len(skills)}", True, YELLOW)
        score_box = pygame.Rect(15, 15, score_surface.get_width() + 20, score_surface.get_height() + 10)
        pygame.draw.rect(screen, WHITE, score_box, 2)
        screen.blit(score_surface, (score_box.x + 10, score_box.y + 5))

        # Bottom message
        if message and pygame.time.get_ticks() - message_timer < 2000:
            show_message(message)

        pygame.display.update()
        clock.tick(snake_speed)

        if won_timer_started and pygame.time.get_ticks() - won_timer_started > 2000:
            show_game_won()


# Start with the intro screen
show_intro_screen()
main()
