import pygame
import sys
# ----------------- GAME SETUP -----------------
pygame.init()
WIDTH, HEIGHT = 2000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ballie - ball Physics")
# Colors
BLACK = (0, 0, 0)

# ----------------- BALL IMAGE -----------------
# Make sure "ball.png" is in the same folder as this file
ball_img = pygame.image.load("mk.png").convert_alpha()

# ----------------- BALL SETTINGS -----------------
ball_radius = 140
ball_x = WIDTH // 2
ball_y = HEIGHT - ball_radius - 200  # Start above floor
ball_velocity_x = 0.0
ball_velocity_y = 0.0

gravity = 0.5
move_accel = 1.0       # Horizontal acceleration
max_speed = 25         # Max horizontal speed
friction = 0.98        # Air friction
ground_friction = 0.9  # Stronger friction when sliding on ground
jump_strength = -20

# Stop threshold for ending small bounces
BOUNCE_STOP_THRESHOLD = 2.0 

# Radii for squash/stretch
radius_x = ball_radius
radius_y = ball_radius

# ----------------- CLOCK -----------------
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

    # Pre-jump squash (ball compresses slightly before launch)
    if keys[pygame.K_UP] and is_on_ground:
        radius_y = ball_radius * 0.85  # Slight vertical compress
        radius_x = ball_radius * 1.15  # Slight horizontal stretch
        ball_velocity_y = jump_strength

    # Horizontal movement
    if keys[pygame.K_LEFT]:
        ball_velocity_x -= move_accel
    if keys[pygame.K_RIGHT]:
        ball_velocity_x += move_accel

    # Limit horizontal speed
    if ball_velocity_x > max_speed:
        ball_velocity_x = max_speed
    elif ball_velocity_x < -max_speed:
        ball_velocity_x = -max_speed

    # ----------------- PHYSICS -----------------
    ball_velocity_y += gravity  # Gravity

    # Air vs Ground friction
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
                radius_y = ball_radius * 0.85  # softer squash
                radius_x = ball_radius * 1.15  # softer stretch

        # Ceiling collision
        elif ball_y <= ball_radius:
            ball_y = ball_radius
            ball_velocity_y = -ball_velocity_y * 0.7
            radius_y = ball_radius * 0.85
            radius_x = ball_radius * 1.15

        # Left wall
        if ball_x <= ball_radius:
            ball_x = ball_radius
            ball_velocity_x = -ball_velocity_x * 0.7
            radius_x = ball_radius * 0.85
            radius_y = ball_radius * 1.15

        # Right wall
        elif ball_x >= WIDTH - ball_radius:
            ball_x = WIDTH - ball_radius
            ball_velocity_x = -ball_velocity_x * 0.7
            radius_x = ball_radius * 0.85
            radius_y = ball_radius * 1.15

    # ----------------- SHAPE RESTORATION -----------------
    restore_rate = 0.2
    is_sliding_slowly = abs(ball_velocity_x) < 2.0

    # Snap shape instantly if nearly settled
    if is_on_ground and is_sliding_slowly:
        restore_rate = 1.0

    # Restore toward normal shape
    radius_x += (ball_radius - radius_x) * restore_rate
    radius_y += (ball_radius - radius_y) * restore_rate

    # Avoid negative scaling (just a safety)
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

    # Optional soft shadow
    shadow_width = int(radius_x * 2.2)
    shadow_height = int(radius_y * 0.3)
    shadow = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 0, 0, 120), shadow.get_rect())
    screen.blit(shadow, (ball_x - shadow_width / 2, HEIGHT - shadow_height - 5))

    # Draw the PNG ball with current squash/stretch
    scaled_ball = pygame.transform.smoothscale(ball_img, (int(radius_x * 2), int(radius_y * 2)))
    screen.blit(scaled_ball, (ball_x - radius_x, ball_y - radius_y))

    pygame.display.flip()
    clock.tick(100)
