import pygame
import sys

# ----------------- GAME SETUP -----------------
pygame.init()

WIDTH, HEIGHT = 2000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ballie - Bouncing Ball with Squash")

# Colors
BLACK = (0, 0, 0)
RED   = (0,255,0)

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

# Threshold for stopping tiny bounces and settling the ball on the ground.
# Must be greater than gravity to prevent immediate re-collision.
BOUNCE_STOP_THRESHOLD = 2.0 

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

    # Jump from ground (Note: This is sensitive to the ball_y position)
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
    # If this is true, the ball is actively in motion, and we allow squash/stretch effects
    moving = abs(ball_velocity_x) > 0.1 or abs(ball_velocity_y) > 0.1

    # Only apply collision squash if moving
    if moving:
        # Bottom collision (Ground)
        if ball_y >= HEIGHT - ball_radius:
            ball_y = HEIGHT - ball_radius
            
            # Check if velocity is low enough to stop bouncing
            if abs(ball_velocity_y) < BOUNCE_STOP_THRESHOLD:
                ball_velocity_y = 0.0 # Force vertical stop
            else:
                # Normal bounce with energy loss and squash
                ball_velocity_y = -ball_velocity_y * 0.7
                radius_y = ball_radius * 0.7  # squash vertically
                radius_x = ball_radius * 1.3  # stretch horizontally
        
        # Top wall
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

    # --- SHAPE RESTORATION (The Fix) ---
    
    # Default rate for gradual restoration when mid-air or moving fast
    restore_rate = 0.2

    # Check if the ball is resting vertically on the ground
    is_on_ground = ball_y >= HEIGHT - ball_radius - 1 

    # Check if the ball is only sliding slowly horizontally
    # We use a higher threshold (2.0) than the 'moving' check (0.1) to catch slow slides.
    is_sliding_slowly = abs(ball_velocity_x) < 2.0 
    
    # MODIFIED: If settled on the ground and moving slowly, snap the shape instantly (rate = 1.0)
    if is_on_ground and is_sliding_slowly:
        restore_rate = 1.0 

    # Apply restoration
    radius_x += (ball_radius - radius_x) * restore_rate
    radius_y += (ball_radius - radius_y) * restore_rate
    
    # Ensure radii don't accidentally become negative due to floating point math
    radius_x = max(0.1, radius_x)
    radius_y = max(0.1, radius_y)


    # If ball is practically stopped (velocity below threshold), force perfect round and zero velocity
    moving = abs(ball_velocity_x) > 0.1 or abs(ball_velocity_y) > 0.1
    if not moving:
        # Final, absolute snap to stop and round shape
        radius_x = ball_radius
        radius_y = ball_radius
        ball_velocity_x = 0
        ball_velocity_y = 0
        # Ensure it's perfectly snapped to the floor if it's the resting surface
        if ball_y > HEIGHT - ball_radius:
             ball_y = HEIGHT - ball_radius


    # ----------------- DRAW -----------------
    screen.fill(BLACK)
    pygame.draw.ellipse(screen, RED, 
        (ball_x - radius_x, ball_y - radius_y, radius_x*2, radius_y*2))

    pygame.display.flip()
    clock.tick(100)
