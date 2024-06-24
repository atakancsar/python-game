import pygame
import random

# Pygame'i başlat
pygame.init()

# Ekran boyutları
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 255, 0)
BLUE_SKY = (135, 206, 235)
LIGHT_BLUE = (173, 216, 230)

# Font
font = pygame.font.SysFont(None, 55)

# Kuş parametreleri
bird_x = 50
bird_y = 300
bird_width = 30
bird_height = 30
bird_velocity = 0
gravity = 0.5

# Oyun durumu
running = True
game_active = False
score = 0

# FPS ayarı
clock = pygame.time.Clock()

# Pipe management
pipes = []
spawn_pipe_x = SCREEN_WIDTH
pipe_velocity = 3

# Background elements
mountains = []
mountain_velocity = 1
clouds = [(300, 100), (450, 50), (600, 150)]
cloud_velocity = 2

def generate_mountain():
    base_height = 400
    peak_height = random.randint(250, 350)
    width = random.randint(100, 200)
    return (base_height, peak_height, width)

def initialize_mountains():
    x_position = 0
    for _ in range(4):  # Initialize four mountains
        base_height, peak_height, width = generate_mountain()
        mountains.append((x_position, base_height, peak_height, width))
        x_position += width

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def reset_game():
    global bird_y, bird_velocity, score, pipes, mountains, clouds
    bird_y = 300
    bird_velocity = 0
    score = 0
    pipes = [{'x': SCREEN_WIDTH, 'height': random.randint(150, 400), 'gap': random.randint(150, 250)}]
    mountains.clear()
    initialize_mountains()
    clouds = [(300, 100), (450, 50), (600, 150)]

def draw_bird(x, y):
    pygame.draw.ellipse(screen, YELLOW, (x, y, bird_width, bird_height))
    pygame.draw.circle(screen, BLACK, (x + 22, y + 10), 5)

def manage_pipes():
    global score
    for pipe in pipes:
        pipe['x'] -= pipe_velocity
    if pipes[0]['x'] + 70 < 0:  # Pipe width is 70
        pipes.pop(0)
        score += 1
    if len(pipes) < 2:  # Always keep one pipe ready off-screen
        last_pipe_x = pipes[-1]['x']
        pipes.append({'x': last_pipe_x + 300, 'height': random.randint(150, 400), 'gap': random.randint(150, 250)})

def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe['x'], 0, 70, pipe['height']))
        pygame.draw.rect(screen, GREEN, (pipe['x'], pipe['height'] + pipe['gap'], 70, SCREEN_HEIGHT - pipe['height'] - pipe['gap']))
        # Add some details to pipes
        pygame.draw.rect(screen, DARK_GREEN, (pipe['x'], pipe['height'] - 20, 70, 20))
        pygame.draw.rect(screen, DARK_GREEN, (pipe['x'], pipe['height'] + pipe['gap'], 70, 20))

def draw_background():
    # Draw sky
    screen.fill(BLUE_SKY)
    # Draw clouds
    for cloud in clouds:
        pygame.draw.ellipse(screen, LIGHT_BLUE, (cloud[0], cloud[1], 100, 50))
    # Draw mountains
    for mountain in mountains:
        x, base_height, peak_height, width = mountain
        pygame.draw.polygon(screen, DARK_GREEN, [(x, 600), (x + width // 2, peak_height), (x + width, 600)])

def update_background():
    global mountains, clouds
    # Update mountains
    mountains = [(mountain[0] - mountain_velocity, mountain[1], mountain[2], mountain[3]) for mountain in mountains]
    if mountains[0][0] + mountains[0][3] < 0:  # Check if the first mountain is off screen
        mountains.pop(0)
        base_height, peak_height, width = generate_mountain()
        last_x = mountains[-1][0] + mountains[-1][3]
        mountains.append((last_x, base_height, peak_height, width))
    # Update clouds
    clouds = [(cloud[0] - cloud_velocity, cloud[1]) for cloud in clouds]
    if clouds[0][0] + 100 < 0:  # Cloud width is 100
        clouds.pop(0)
        clouds.append((clouds[-1][0] + 250, random.randint(50, 150)))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_active:
                    game_active = True
                    reset_game()
                bird_velocity = -10

    if game_active:
        bird_velocity += gravity
        bird_y += bird_velocity
        manage_pipes()
        update_background()

        # Collision detection
        for pipe in pipes:
            if (bird_y < 0 or bird_y + bird_height > SCREEN_HEIGHT or
                (pipe['x'] < bird_x + bird_width < pipe['x'] + 70 and
                 (bird_y < pipe['height'] or bird_y + bird_height > pipe['height'] + pipe['gap']))):
                game_active = False

    draw_background()

    if game_active:
        draw_bird(bird_x, bird_y)
        draw_pipes()
        draw_text(f"Score: {score}", font, BLACK, screen, 10, 10)
    else:
        draw_text("Press SPACE to Start", font, BLACK, screen, 50, SCREEN_HEIGHT // 2 - 50)
        draw_text(f"Score: {score}", font, BLACK, screen, 150, SCREEN_HEIGHT // 2 + 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()