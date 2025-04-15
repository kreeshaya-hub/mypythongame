import pygame
import random

pygame.init()

# Screen settings
WIDTH, HEIGHT = 1080, 720
BLOCK_SIZE = 60
MARGIN_BLOCKS = 2
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
ORANGE = (255, 165, 0)

# Game settings
clock = pygame.time.Clock()

# Add these constants near the top with other game settings
DIFFICULTY_LEVELS = {
    'Easy': {
        'speed': 4,
        'scroll_speed': 2,
        'points_per_skill': 1,
        'color': (0, 255, 0),  # GREEN
        'num_obstacles': 1  # Only one obstacle at a time
    },
    'Medium': {
        'speed': 4,
        'scroll_speed': 4,
        'points_per_skill': 2,
        'color': (255, 165, 0),  # ORANGE
        'num_obstacles': 2  # 2-3 obstacles
    },
    'Hard': {
        'speed': 4,
        'scroll_speed': 6,
        'points_per_skill': 3,
        'color': (255, 0, 0),  # RED
        'num_obstacles': 5  # 5-6 obstacles
    }
}

# Fonts (safe fallback for Web)
font = pygame.font.Font(None, 24)
big_font = pygame.font.Font(None, 48)

# Load skill icons
skills = [
    {"name": "Python", "icon": pygame.image.load("icons/Python.png")},
    {"name": "Figma", "icon": pygame.image.load("icons/Figma.png")},
    {"name": "React", "icon": pygame.image.load("icons/React.png")},
    {"name": "JavaScript", "icon": pygame.image.load("icons/JavaScript.png")},
    {"name": "Wordpress", "icon": pygame.image.load("icons/Wordpress.png")},
    {"name": "Node.js", "icon": pygame.image.load("icons/nodejs.png")},
    {"name": "GitHub", "icon": pygame.image.load("icons/github.png")},
    {"name": "After Effects", "icon": pygame.image.load("icons/after-effects.png")},
    {"name": "Photoshop", "icon": pygame.image.load("icons/photoshop.png")},
    {"name": "Illustrator", "icon": pygame.image.load("icons/illustrator.png")},
    {"name": "Audition", "icon": pygame.image.load("icons/audition.png")},
    {"name": "Premiere Pro", "icon": pygame.image.load("icons/premiere-pro.png")},
    {"name": "MongoDB", "icon": pygame.image.load("icons/mongodb.png")},
]

for skill in skills:
    skill["icon"] = pygame.transform.scale(skill["icon"], (BLOCK_SIZE, BLOCK_SIZE))

# Add after the skills list
OBSTACLES = [
    {"name": "Tree", "color": (34, 139, 34), "points": [
        (BLOCK_SIZE//2, 0),  # Top of tree
        (BLOCK_SIZE, BLOCK_SIZE),  # Bottom right
        (0, BLOCK_SIZE)  # Bottom left
    ]},
    {"name": "Rock", "color": (128, 128, 128), "points": [
        (BLOCK_SIZE//4, 0),  # Top left
        (3*BLOCK_SIZE//4, 0),  # Top right
        (BLOCK_SIZE, BLOCK_SIZE//2),  # Middle right
        (3*BLOCK_SIZE//4, BLOCK_SIZE),  # Bottom right
        (BLOCK_SIZE//4, BLOCK_SIZE),  # Bottom left
        (0, BLOCK_SIZE//2)  # Middle left
    ]},
    {"name": "Bone", "color": (255, 250, 250), "shape": "bone"}
]

# Number of obstacles to place
NUM_OBSTACLES = 5

# Add after NUM_OBSTACLES
obstacles = []  # Global list to store obstacles

# Update these constants
BORDER_THICKNESS = 15  # Thicker border
BORDER_COLOR = (255, 69, 0)  # Red-orange color (like lava)
MOVEMENT_SPEED = BLOCK_SIZE  # Full block movement for precise control
SCROLL_SPEED = 2  # Speed of downward scrolling for obstacles and skills
HORIZONTAL_SPEED = BLOCK_SIZE  # Speed for left/right movement
VIEWPORT_HEIGHT = HEIGHT
SCROLL_Y = 0  # Track total scroll distance

def draw_snake(body, direction, scroll_y):
    # Draw body segments first (from tail to head)
    for i, block in enumerate(body[1:], 1):  # Skip the head, draw only body
        x, y = block[0], block[1]
        if 0 <= y <= HEIGHT:  # Only draw if in viewport
            body_color = DIFFICULTY_LEVELS[current_difficulty]['color']
            dark_body_color = (
                max(0, body_color[0] - 40),
                max(0, body_color[1] - 40),
                max(0, body_color[2] - 40)
            )
            
            # Draw a rounded rectangle for body segment
            pygame.draw.rect(screen, dark_body_color, 
                           pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE),
                           border_radius=10)
            
            # Add a smaller inner rectangle for detail
            pygame.draw.rect(screen, body_color,
                           pygame.Rect(x + 4, y + 4, BLOCK_SIZE - 8, BLOCK_SIZE - 8),
                           border_radius=8)

    # Draw head last (so it's always on top)
    head_x, head_y = body[0][0], body[0][1]
    if 0 <= head_y <= HEIGHT:
        head_color = DIFFICULTY_LEVELS[current_difficulty]['color']
        
        # Draw head base (circle)
        pygame.draw.circle(screen, head_color,
                         (head_x + BLOCK_SIZE//2, head_y + BLOCK_SIZE//2),
                         BLOCK_SIZE//2)
        
        # Draw directional triangle for head
        if direction == 'RIGHT':
            points = [
                (head_x + BLOCK_SIZE, head_y + BLOCK_SIZE//2),  # Tip
                (head_x + BLOCK_SIZE//2, head_y),  # Top
                (head_x + BLOCK_SIZE//2, head_y + BLOCK_SIZE)  # Bottom
            ]
        elif direction == 'LEFT':
            points = [
                (head_x, head_y + BLOCK_SIZE//2),  # Tip
                (head_x + BLOCK_SIZE//2, head_y),  # Top
                (head_x + BLOCK_SIZE//2, head_y + BLOCK_SIZE)  # Bottom
            ]
        elif direction == 'UP':
            points = [
                (head_x + BLOCK_SIZE//2, head_y),  # Tip
                (head_x, head_y + BLOCK_SIZE//2),  # Left
                (head_x + BLOCK_SIZE, head_y + BLOCK_SIZE//2)  # Right
            ]
        else:  # DOWN
            points = [
                (head_x + BLOCK_SIZE//2, head_y + BLOCK_SIZE),  # Tip
                (head_x, head_y + BLOCK_SIZE//2),  # Left
                (head_x + BLOCK_SIZE, head_y + BLOCK_SIZE//2)  # Right
            ]
        
        pygame.draw.polygon(screen, head_color, points)
        
        # Add eyes
        eye_color = BLACK
        eye_size = 4
        if direction == 'RIGHT':
            pygame.draw.circle(screen, eye_color, 
                             (head_x + 3*BLOCK_SIZE//4, head_y + BLOCK_SIZE//3), eye_size)
            pygame.draw.circle(screen, eye_color, 
                             (head_x + 3*BLOCK_SIZE//4, head_y + 2*BLOCK_SIZE//3), eye_size)
        elif direction == 'LEFT':
            pygame.draw.circle(screen, eye_color, 
                             (head_x + BLOCK_SIZE//4, head_y + BLOCK_SIZE//3), eye_size)
            pygame.draw.circle(screen, eye_color, 
                             (head_x + BLOCK_SIZE//4, head_y + 2*BLOCK_SIZE//3), eye_size)
        elif direction == 'UP':
            pygame.draw.circle(screen, eye_color, 
                             (head_x + BLOCK_SIZE//3, head_y + BLOCK_SIZE//4), eye_size)
            pygame.draw.circle(screen, eye_color, 
                             (head_x + 2*BLOCK_SIZE//3, head_y + BLOCK_SIZE//4), eye_size)
        else:  # DOWN
            pygame.draw.circle(screen, eye_color, 
                             (head_x + BLOCK_SIZE//3, head_y + 3*BLOCK_SIZE//4), eye_size)
            pygame.draw.circle(screen, eye_color, 
                             (head_x + 2*BLOCK_SIZE//3, head_y + 3*BLOCK_SIZE//4), eye_size)


def draw_border():
    # Draw outer border
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, WIDTH, HEIGHT), BORDER_THICKNESS)
    
    # Add lava effect (optional animated circles in the border)
    for i in range(0, WIDTH, BORDER_THICKNESS * 2):
        y_positions = [0, HEIGHT - BORDER_THICKNESS]
        for y in y_positions:
            pygame.draw.circle(screen, (255, 140, 0), 
                             (i + (pygame.time.get_ticks() // 100 % BORDER_THICKNESS * 2), y + BORDER_THICKNESS//2), 
                             BORDER_THICKNESS//2)
    
    for i in range(0, HEIGHT, BORDER_THICKNESS * 2):
        x_positions = [0, WIDTH - BORDER_THICKNESS]
        for x in x_positions:
            pygame.draw.circle(screen, (255, 140, 0), 
                             (x + BORDER_THICKNESS//2, i + (pygame.time.get_ticks() // 100 % BORDER_THICKNESS * 2)), 
                             BORDER_THICKNESS//2)


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
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return


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
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return


def get_safe_position(active_obstacles, current_skill_pos=None, min_distance=BLOCK_SIZE * 3):
    """Get a position that's safely away from obstacles and current skill"""
    while True:
        x = random.randrange(MARGIN_BLOCKS, (WIDTH // BLOCK_SIZE) - MARGIN_BLOCKS) * BLOCK_SIZE
        y = random.randrange(MARGIN_BLOCKS, (HEIGHT // BLOCK_SIZE) - MARGIN_BLOCKS) * BLOCK_SIZE
        
        # Check distance from obstacles
        is_safe = True
        for obstacle in active_obstacles:
            dist_x = abs(obstacle['x'] - x)
            dist_y = abs(obstacle['y'] - y)
            if dist_x < min_distance and dist_y < min_distance:
                is_safe = False
                break
        
        # Check distance from current skill
        if current_skill_pos and is_safe:
            skill_x, skill_y = current_skill_pos
            dist_x = abs(skill_x - x)
            dist_y = abs(skill_y - y)
            if dist_x < min_distance and dist_y < min_distance:
                is_safe = False
        
        if is_safe:
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
            "1. Use arrow keys to change direction!",
            "2. Snake moves continuously in the last direction pressed.",
            "3. Collect skills to grow longer and score points.",
            "4. Avoid obstacles and the lava border!",
            "5. Enjoy my Game!!"
        ]

        for i, line in enumerate(instructions):
            instr_text = font.render(line, True, WHITE)
            screen.blit(instr_text, (WIDTH // 2 - instr_text.get_width() // 2, HEIGHT // 3 + i * 30))

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
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    button_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if button_rect.collidepoint(event.pos) and button_pressed:
                    return
                button_pressed = False


def show_difficulty_select():
    button_height = 50
    button_width = 200
    button_margin = 20
    total_height = (button_height + button_margin) * len(DIFFICULTY_LEVELS)
    start_y = (HEIGHT - total_height) // 2

    buttons = {}
    
    while True:
        screen.fill(BLACK)
        draw_border()
        
        title_text = big_font.render("Select Difficulty", True, GOLD)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, start_y - 80))

        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True

        y = start_y
        for difficulty in DIFFICULTY_LEVELS:
            button_rect = pygame.Rect(
                WIDTH // 2 - button_width // 2,
                y,
                button_width,
                button_height
            )
            buttons[difficulty] = button_rect
            
            # Change button color on hover
            if button_rect.collidepoint(mouse_pos):
                button_color = DIFFICULTY_LEVELS[difficulty]['color']
                if mouse_clicked:
                    return difficulty
            else:
                button_color = DARK_GREEN

            pygame.draw.rect(screen, button_color, button_rect)
            
            # Draw difficulty text
            diff_text = font.render(difficulty, True, BLACK)
            screen.blit(diff_text, (
                button_rect.centerx - diff_text.get_width() // 2,
                button_rect.centery - diff_text.get_height() // 2
            ))
            
            # Draw difficulty info
            info_text = font.render(
                f"Speed: {DIFFICULTY_LEVELS[difficulty]['speed']} | Points: {DIFFICULTY_LEVELS[difficulty]['points_per_skill']}x",
                True, WHITE
            )
            screen.blit(info_text, (
                WIDTH // 2 - info_text.get_width() // 2,
                button_rect.bottom + 5
            ))
            
            y += button_height + button_margin
        
        pygame.display.update()


def draw_obstacle(obstacle_type, x, y):
    if obstacle_type["name"] == "Bone":
        # Draw a bone shape
        color = obstacle_type["color"]
        # Main bone body
        pygame.draw.ellipse(screen, color, 
                          (x + BLOCK_SIZE//4, y + BLOCK_SIZE//3, 
                           BLOCK_SIZE//2, BLOCK_SIZE//3))
        # Bone ends
        pygame.draw.circle(screen, color, 
                         (x + BLOCK_SIZE//4, y + BLOCK_SIZE//2), 
                         BLOCK_SIZE//4)
        pygame.draw.circle(screen, color, 
                         (x + 3*BLOCK_SIZE//4, y + BLOCK_SIZE//2), 
                         BLOCK_SIZE//4)
    else:
        # Draw polygon obstacles
        points = [(x + dx, y + dy) for dx, dy in obstacle_type["points"]]
        pygame.draw.polygon(screen, obstacle_type["color"], points)


def play_death_animation(snake_body, collision_point, direction, current_skill=None, skill_x=0, skill_y=0):
    fade_steps = 10  # Number of fade steps
    fall_steps = 15  # Number of falling steps
    original_color = DIFFICULTY_LEVELS[current_difficulty]['color']
    
    # Fade and fall animation
    for step in range(max(fade_steps, fall_steps)):
        screen.fill(BLACK)
        draw_border()
        
        # Draw obstacles
        for obstacle in obstacles:
            draw_obstacle(obstacle['type'], obstacle['x'], obstacle['y'])
        
        # Calculate fade color
        if step < fade_steps:
            fade_factor = 1 - (step / fade_steps)
            current_color = (
                int(original_color[0] * fade_factor),
                int(original_color[1] * fade_factor),
                int(original_color[2] * fade_factor)
            )
        else:
            current_color = (50, 50, 50)  # Very dark gray
        
        # Draw falling snake
        for i, segment in enumerate(snake_body):
            fall_delay = i * 2  # Delayed fall for each segment
            if step > fall_delay:
                fall_amount = min((step - fall_delay) * 3, HEIGHT - segment[1])
                segment_y = segment[1] + fall_amount
            else:
                segment_y = segment[1]
                
            # Draw body segment
            pygame.draw.rect(screen, current_color,
                           pygame.Rect(segment[0] + 4, segment_y + 4,
                                     BLOCK_SIZE - 8, BLOCK_SIZE - 8),
                           border_radius=8)
        
        # Draw current skill if exists
        if current_skill:
            screen.blit(current_skill["icon"], (skill_x, skill_y))
        
        # Display score and difficulty
        score_text = font.render(f"Score: {score}", True, YELLOW)
        diff_text = font.render(f"Difficulty: {current_difficulty}", True, 
                              DIFFICULTY_LEVELS[current_difficulty]['color'])
        screen.blit(score_text, (15, 15))
        screen.blit(diff_text, (15, 45))
        
        pygame.display.update()
        pygame.time.delay(50)  # Slow down the animation


def show_countdown():
    countdown_from = 3
    for i in range(countdown_from, 0, -1):
        screen.fill(BLACK)
        draw_border()
        
        # Draw "Get Ready!" text
        ready_text = big_font.render("Get Ready!", True, GOLD)
        screen.blit(ready_text, (WIDTH // 2 - ready_text.get_width() // 2, HEIGHT // 3))
        
        # Draw countdown number
        count_text = big_font.render(str(i), True, WHITE)
        screen.blit(count_text, (WIDTH // 2 - count_text.get_width() // 2, HEIGHT // 2))
        
        pygame.display.update()
        pygame.time.delay(1000)  # Wait for 1 second

    # Show "GO!" text
    screen.fill(BLACK)
    draw_border()
    go_text = big_font.render("GO!", True, GREEN)
    screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(500)  # Show "GO!" for half a second


def main():
    global snake_speed, current_difficulty, score, obstacles
    
    # Reset game state
    obstacles = []
    
    # Initial setup
    selected_difficulty = show_difficulty_select()
    if selected_difficulty is None:
        return
    
    current_difficulty = selected_difficulty
    snake_speed = 4  # Set snake speed to 4 for all difficulties
    scroll_speed = DIFFICULTY_LEVELS[current_difficulty]['scroll_speed']
    score = 0

    # Show countdown before starting
    show_countdown()

    # Start snake with just the head
    snake_pos = [WIDTH // 2, HEIGHT - 2 * BLOCK_SIZE]
    snake_body = [list(snake_pos)]
    body_length = 1
    direction = 'UP'  # Start moving upward
    
    # Track movement direction
    dx = 0
    dy = -BLOCK_SIZE  # Start moving up

    # Initialize first skill
    remaining_skills = skills.copy()
    current_skill = random.choice(remaining_skills)
    skill_x = random.randrange(MARGIN_BLOCKS, (WIDTH // BLOCK_SIZE) - MARGIN_BLOCKS) * BLOCK_SIZE
    skill_y = random.randrange(MARGIN_BLOCKS, (HEIGHT // BLOCK_SIZE) - MARGIN_BLOCKS) * BLOCK_SIZE

    # Generate initial obstacles with better spacing
    active_obstacles = []
    for i in range(DIFFICULTY_LEVELS[current_difficulty]['num_obstacles']):
        if i == 0:
            obs_x, obs_y = get_safe_position(active_obstacles)
        else:
            obs_x, obs_y = get_safe_position(active_obstacles, (skill_x, skill_y))
        
        obs_y = -BLOCK_SIZE - (i * HEIGHT // DIFFICULTY_LEVELS[current_difficulty]['num_obstacles'])
        active_obstacles.append({
            'type': random.choice(OBSTACLES),
            'x': obs_x,
            'y': obs_y
        })

    message = ""
    message_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'
                    dx = BLOCK_SIZE
                    dy = 0
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                    dx = -BLOCK_SIZE
                    dy = 0
                elif event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                    dx = 0
                    dy = -BLOCK_SIZE
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'
                    dx = 0
                    dy = BLOCK_SIZE

        # Move snake in current direction
        new_x = snake_pos[0] + dx
        new_y = snake_pos[1] + dy

        # Keep snake within bounds
        new_x = max(BORDER_THICKNESS, min(new_x, WIDTH - BLOCK_SIZE - BORDER_THICKNESS))
        new_y = max(BORDER_THICKNESS, min(new_y, HEIGHT - BLOCK_SIZE - BORDER_THICKNESS))

        # Update snake position
        snake_pos[0] = new_x
        snake_pos[1] = new_y

        # Update snake body (only if we have segments to add)
        snake_body.insert(0, list(snake_pos))
        if len(snake_body) > body_length:  # Only keep as many segments as we've earned
            snake_body.pop()

        # Check border collision (make it more strict)
        if (snake_pos[0] <= BORDER_THICKNESS or 
            snake_pos[0] >= WIDTH - BLOCK_SIZE - BORDER_THICKNESS or
            snake_pos[1] <= BORDER_THICKNESS or 
            snake_pos[1] >= HEIGHT - BLOCK_SIZE - BORDER_THICKNESS):
            play_death_animation(snake_body, snake_pos, direction, current_skill, skill_x, skill_y)
            show_game_over()
            return

        # Also check if any part of the snake touches the border
        head_rect = pygame.Rect(snake_pos[0], snake_pos[1], BLOCK_SIZE, BLOCK_SIZE)
        border_rects = [
            pygame.Rect(0, 0, WIDTH, BORDER_THICKNESS),  # Top border
            pygame.Rect(0, HEIGHT - BORDER_THICKNESS, WIDTH, BORDER_THICKNESS),  # Bottom border
            pygame.Rect(0, 0, BORDER_THICKNESS, HEIGHT),  # Left border
            pygame.Rect(WIDTH - BORDER_THICKNESS, 0, BORDER_THICKNESS, HEIGHT)  # Right border
        ]
        
        for border in border_rects:
            if head_rect.colliderect(border):
                play_death_animation(snake_body, snake_pos, direction, current_skill, skill_x, skill_y)
                show_game_over()
                return

        # Check obstacle collisions with more precise detection
        for obstacle in active_obstacles:
            obstacle_rect = pygame.Rect(
                obstacle['x'] - 5,
                obstacle['y'] - 5,
                BLOCK_SIZE + 10,
                BLOCK_SIZE + 10
            )
            if head_rect.colliderect(obstacle_rect):
                play_death_animation(snake_body, snake_pos, direction, current_skill, skill_x, skill_y)
                show_game_over()
                return

        # Check self collision (snake hitting itself)
        for segment in snake_body[1:]:  # Skip the head
            if snake_pos[0] == segment[0] and snake_pos[1] == segment[1]:
                play_death_animation(snake_body, snake_pos, direction, current_skill, skill_x, skill_y)
                show_game_over()
                return

        # Check skill collection
        if current_skill:
            skill_rect = pygame.Rect(skill_x, skill_y, BLOCK_SIZE, BLOCK_SIZE)
            if head_rect.colliderect(skill_rect):
                remaining_skills.remove(current_skill)
                score += DIFFICULTY_LEVELS[current_difficulty]['points_per_skill']
                body_length += 1  # Grow snake by one segment

                if not remaining_skills:
                    # Immediately show winning screen when all skills are collected
                    show_game_won()
                    return
                else:
                    message = f"You found {current_skill['name']}! Score: {score}"
                    message_timer = pygame.time.get_ticks()
                    current_skill = random.choice(remaining_skills)
                    # Get new safe position for skill
                    skill_x, skill_y = get_safe_position(active_obstacles)

        # Move obstacles and handle recycling
        for obstacle in active_obstacles:
            obstacle['y'] += scroll_speed
            if obstacle['y'] > HEIGHT:
                # Reset obstacle to top with random x position, ensuring safe distance
                obstacle['y'] = -BLOCK_SIZE
                new_x, _ = get_safe_position(
                    [obs for obs in active_obstacles if obs != obstacle],
                    (skill_x, skill_y)
                )
                obstacle['x'] = new_x
                obstacle['type'] = random.choice(OBSTACLES)

        # Move skill downward with difficulty-based scroll speed
        if current_skill:
            skill_y += scroll_speed
            if skill_y > HEIGHT:
                skill_y = -BLOCK_SIZE
                skill_x, _ = get_safe_position(active_obstacles)

        # Draw game state
        screen.fill(BLACK)
        draw_border()
        
        # Draw obstacles
        for obstacle in active_obstacles:
            draw_obstacle(obstacle['type'], obstacle['x'], obstacle['y'])
        
        # Draw snake
        draw_snake(snake_body, direction, 0)

        # Draw current skill
        if current_skill:
            screen.blit(current_skill["icon"], (skill_x, skill_y))

        # Display score and difficulty
        score_text = font.render(f"Score: {score}", True, YELLOW)
        diff_text = font.render(f"Difficulty: {current_difficulty}", True, 
                              DIFFICULTY_LEVELS[current_difficulty]['color'])
        screen.blit(score_text, (15, 15))
        screen.blit(diff_text, (15, 45))

        if message and pygame.time.get_ticks() - message_timer < 2000:
            show_message(message)

        pygame.display.update()
        clock.tick(snake_speed)


show_intro_screen()
main()
