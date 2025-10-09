import pygame
import sys

# ----------------- GAMEss SETUP -----------------
pygame.init()  # Initiallize Pygame library

WIDTH, HEIGHT = 2000, 1000  # Screen dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create game window
pygame.display.set_caption("Ballie - The Bouncing Ball")  # Window title

# Colors in RGB
BLACK = (0, 0, 0)
RED   = (255, 0, 0)

# ----------------- BALL SETTINGS -----------------
ball_radius = 50
ball_x = WIDTH // 2
ball_y = HEIGHT - ball_radius  # Start visible at bottom
ball_velocity_x = 0.0  # Horizontal speed
ball_velocity_y = 0.0  # Vertical speed

gravity = 0.5          # Pixels per frame per frame
move_accel = 1      # Horizontal acceleration per frame
max_speed = 25        # Max horizontal speed
friction = 0.98        # Multiplier for friction
jump_strength = -20     # Upward jump speed

# ----------------- CLOCK -----------------
clock = pygame.time.Clock()  # For controlling FPS

# ----------------- GAME LOOP -----------------
while True:
    # --- EVENT HANDLING ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If window close button clicked
            pygame.quit()
            sys.exit()

    # --- CONTINUOUS KEY PRESS ---
    keys = pygame.key.get_pressed()  # Get all key states

    # Jump only if ball is on ground
    if keys[pygame.K_UP] and ball_y >= HEIGHT - ball_radius - 1:
        ball_velocity_y = jump_strength

    # Horizontal movement (momentum)
    if keys[pygame.K_LEFT]:
        ball_velocity_x -= move_accel  # Accelerate left
    if keys[pygame.K_RIGHT]:
        ball_velocity_x += move_accel  # Accelerate right

    # Limit horizontal speed
    if ball_velocity_x > max_speed:
        ball_velocity_x = max_speed
    elif ball_velocity_x < -max_speed:
        ball_velocity_x = -max_speed

    # ----------------- PHYSICS -----------------
    # Apply gravity
    ball_velocity_y += gravity

    # Apply friction to horizontal movement
    ball_velocity_x *= friction

    # Update position
    ball_x += ball_velocity_x
    ball_y += ball_velocity_y

    # ----------------- COLLISION / BOUNCE -----------------
    # Bottom & top
    if ball_y >= HEIGHT - ball_radius:
        ball_y = HEIGHT - ball_radius
        ball_velocity_y = -ball_velocity_y * 0.7  # Bounce with energy loss
    elif ball_y <= ball_radius:
        ball_y = ball_radius
        ball_velocity_y = -ball_velocity_y * 0.7

    # Left & right
    if ball_x >= WIDTH - ball_radius:
        ball_x = WIDTH - ball_radius
        ball_velocity_x = -ball_velocity_x * 0.7
    elif ball_x <= ball_radius:
        ball_x = ball_radius
        ball_velocity_x = -ball_velocity_x * 0.7

    # ----------------- DRAW -----------------
    screen.fill(BLACK)  
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)  # Draw ball
    pygame.display.flip()  

    # ----------------- FRAME RATE -----------------
    clock.tick(100) 
