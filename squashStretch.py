import pygame
import sys

# ----------------- GAME SETUP -----------------
pygame.init()

WIDTH, HEIGHT = 2000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ballie - Bouncing Ball with Squash")

# Colors
BLACK = (0, 0, 0)
RED   = (255, 0, 0)

# ----------------- BALL SETTINGS -----------------
ball_radius = 50
ball_x = WIDTH // 2
ball_y = HEIGHT - ball_radius - 200  # Start above floor
ball_velocity_x = 0.0
ball_velocity_y = 0.0

gravity = 0.5
move_accel = 1.0     # horizontal acceleration
max_speed = 25       # max horizontal speed
friction = 0.98      # horizontal friction
jump_strength = -20

# Separate radii for squash/stretch
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

    # Jump from ground
    if keys[pygame.K_UP] and ball_y >= HEIGHT - ball_radius - 1:
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
    # Gravity
    ball_velocity_y += gravity

    # Friction
    ball_velocity_x *= friction

    # Update position
    ball_x += ball_velocity_x
    ball_y += ball_velocity_y

    # ----------------- COLLISION & SQUASH -----------------
    # Determine if ball is practically moving
    moving = abs(ball_velocity_x) > 0.1 or abs(ball_velocity_y) > 0.1

    # Only apply collision squash if moving
    if moving:
        # Bottom & top
        if ball_y >= HEIGHT - ball_radius:
            ball_y = HEIGHT - ball_radius
            ball_velocity_y = -ball_velocity_y * 0.7
            radius_y = ball_radius * 0.7  # squash vertically
            radius_x = ball_radius * 1.3  # stretch horizontally
        elif ball_y <= ball_radius:
            ball_y = ball_radius
            ball_velocity_y = -ball_velocity_y * 0.7
            radius_y = ball_radius * 0.7
            radius_x = ball_radius * 1.3

        # Left & right walls
        if ball_x >= WIDTH - ball_radius:
            ball_x = WIDTH - ball_radius
            ball_velocity_x = -ball_velocity_x * 0.7
            radius_x = ball_radius * 0.7  # squash horizontally
            radius_y = ball_radius * 1.3  # stretch vertically
        elif ball_x <= ball_radius:
            ball_x = ball_radius
            ball_velocity_x = -ball_velocity_x * 0.7
            radius_x = ball_radius * 0.7
            radius_y = ball_radius * 1.3

    # Gradually restore shape
    radius_x += (ball_radius - radius_x) * 0.2
    radius_y += (ball_radius - radius_y) * 0.2

    # If ball is practically stopped, force perfect round
    if not moving:
        radius_x = ball_radius
        radius_y = ball_radius
        ball_velocity_x = 0
        ball_velocity_y = 0

    # ----------------- DRAW -----------------
    screen.fill(BLACK)
    pygame.draw.ellipse(screen, RED, 
        (ball_x - radius_x, ball_y - radius_y, radius_x*2, radius_y*2))

    pygame.display.flip()
    clock.tick(100)
