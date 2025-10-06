import pygame
import sys

# ----------------- GAME SETUP -----------------

pygame.init()

WIDTH, HEIGHT = 200, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ballie")

BLACK = (0, 0, 0)
RED   = (255, 0, 0)

# ----------------- BALL SETTINGS -----------------

ball_radius = 50
ball_x = WIDTH // 2
ball_y = HEIGHT - ball_radius
ball_velocity_x = 0
ball_velocity_y = 0.0  # Use float for smoother physics
gravity = 0.5
move_speed = 5

# ----------------- CLOCK SETTINGS -----------------

clock = pygame.time.Clock()

# ----------------- GAME LOOP -----------------

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- Continuous Input Handling (should be outside the event loop) ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and ball_y >= HEIGHT - ball_radius: # Allow jump only from ground
        ball_velocity_y = -20     # A strong upward jump
    if keys[pygame.K_LEFT]:
        ball_velocity_x = -move_speed      # move left
    if keys[pygame.K_RIGHT]:
        ball_velocity_x = move_speed       # move right
    
      
    # ----------------- PHYSICS -----------------

    # Apply gravity
    ball_velocity_y += gravity

    #friction
    ball_velocity_x *= 0.95  # ✅ Apply friction to slow horizontal movement

    # Update position
    ball_x += ball_velocity_x
    ball_y += ball_velocity_y

    # Boundary checks and bounce
    # Bottom & top
    if ball_y >= HEIGHT - ball_radius:
        ball_y = HEIGHT - ball_radius
        ball_velocity_y = -ball_velocity_y * 0.7  # bounce with some energy loss
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


    # ----------------- DRAWING -----------------

    screen.fill(BLACK)
    pygame.draw.circle(screen, RED, (ball_x, int(ball_y)), ball_radius)
    pygame.display.flip()
    clock.tick(100)
