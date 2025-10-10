import pygame
import sys

# ----------------- GAME SETUP -----------------
pygame.init()
WIDTH, HEIGHT = 2000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ballie - bouncing ball")

# Colors
BLACK = (0, 0, 0)

# ----------------- BALLL SETTINGS -----------------
ball_radius = 140
ball_x = WIDTH // 2
ball_y = HEIGHT - ball_radius - 200
ball_velocity_x = 0.0
ball_velocity_y = 0.0

# ----------------- BALL IMAGE -----------------
ball_img = pygame.image.load("ball.png").convert_alpha()  # keep transparency
ball_img = pygame.transform.smoothscale(ball_img, (ball_radius * 2, ball_radius * 2))

gravity = 0.5
move_accel = 1.0
max_speed = 25
friction = 0.98
ground_friction = 0.9
jump_strength = -20

BOUNCE_STOP_THRESHOLD = 2.0

radius_x = ball_radius
radius_y = ball_radius

clock = pygame.time.Clock()

# ----------------- GAME LOOP -----------------
while True:
    # --- EVENT HANDLING ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- CONTINUOUS KEY PRESS ---
    keys = pygame.key.get_pressed()
    is_on_ground = ball_y >= HEIGHT - ball_radius - 1

    # Pre-jump squash (anticipation)
    if keys[pygame.K_UP] and is_on_ground:
        radius_y = ball_radius * 0.8
        radius_x = ball_radius * 1.2
        ball_velocity_y = jump_strength

    # Horizontal movement
    if keys[pygame.K_LEFT]:
        ball_velocity_x -= move_accel
    if keys[pygame.K_RIGHT]:
        ball_velocity_x += move_accel

    # Limit horizontal speed
    ball_velocity_x = max(-max_speed, min(max_speed, ball_velocity_x))

    # ----------------- PHYSICS -----------------
    ball_velocity_y += gravity

    # Apply friction
    if is_on_ground:
        ball_velocity_x *= ground_friction
    else:
        ball_velocity_x *= friction

    # Update position
    ball_x += ball_velocity_x
    ball_y += ball_velocity_y

    # ----------------- COLLISION & SQUASH -----------------
    moving = abs(ball_velocity_x) > 0.1 or abs(ball_velocity_y) > 0.1

    if moving:
        # Ground collision
        if ball_y >= HEIGHT - ball_radius:
            ball_y = HEIGHT - ball_radius
            if abs(ball_velocity_y) < BOUNCE_STOP_THRESHOLD:
                ball_velocity_y = 0.0
            else:
                ball_velocity_y = -ball_velocity_y * 0.7
                radius_y = ball_radius * 0.7  # more squash
                radius_x = ball_radius * 1.3  # more stretch

        # Ceiling collision
        elif ball_y <= ball_radius:
            ball_y = ball_radius
            ball_velocity_y = -ball_velocity_y * 0.7
            radius_y = ball_radius * 0.7
            radius_x = ball_radius * 1.3

        # Left wall
        if ball_x <= ball_radius:
            ball_x = ball_radius
            ball_velocity_x = -ball_velocity_x * 0.7
            radius_x = ball_radius * 0.7
            radius_y = ball_radius * 1.3

        # Right wall
        elif ball_x >= WIDTH - ball_radius:
            ball_x = WIDTH - ball_radius
            ball_velocity_x = -ball_velocity_x * 0.7
            radius_x = ball_radius * 0.7
            radius_y = ball_radius * 1.3

    # ----------------- SHAPE RESTORATION -----------------
    restore_rate = 0.25
    is_sliding_slowly = abs(ball_velocity_x) < 2.0

    if is_on_ground and is_sliding_slowly:
        restore_rate = 1.0

    radius_x += (ball_radius - radius_x) * restore_rate
    radius_y += (ball_radius - radius_y) * restore_rate

    radius_x = max(0.1, radius_x)
    radius_y = max(0.1, radius_y)

    # ----------------- FINAL SNAP WHEN STOPPED -----------------
    moving = abs(ball_velocity_x) > 0.1 or abs(ball_velocity_y) > 0.1
    if not moving:
        radius_x = ball_radius
        radius_y = ball_radius
        ball_velocity_x = 0
        ball_velocity_y = 0
        if ball_y > HEIGHT - ball_radius:
            ball_y = HEIGHT - ball_radius

    # ----------------- DRAW -----------------
    screen.fill(BLACK)

    # Soft shadow
    shadow_width = int(radius_x * 2.2)
    shadow_height = int(radius_y * 0.3)
    shadow = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 0, 0, 120), shadow.get_rect())
    screen.blit(shadow, (ball_x - shadow_width / 2, HEIGHT - shadow_height - 5))

    # Draw scaled ball
    scaled_ball = pygame.transform.smoothscale(ball_img, (int(radius_x * 2), int(radius_y * 2)))
    screen.blit(scaled_ball, (ball_x - radius_x, ball_y - radius_y))

    pygame.display.flip()
    clock.tick(120)
