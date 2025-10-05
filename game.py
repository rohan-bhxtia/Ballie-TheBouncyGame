import pygame
import sys

# ----------------- GAME SETUP -----------------

pygame.init()

WIDTH, HEIGHT = 2000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ballie")

BLACK = (0, 0, 0)
RED   = (255, 0, 0)

# ----------------- BALL SETTINGS -----------------

ball_radius = 50
ball_x = WIDTH // 2
ball_y = HEIGHT - ball_radius
ball_velocity = 0
gravity = 1
jump_strength = -20

# ----------------- CLOCK SETTINGS -----------------

clock = pygame.time.Clock()

# ----------------- GAME LOOP -----------------

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and ball_y == HEIGHT - ball_radius:
                ball_velocity = jump_strength

    # ----------------- PHYSICS -----------------

    ball_velocity += gravity
    ball_y += ball_velocity

    if ball_y >= HEIGHT - ball_radius:
        ball_y = HEIGHT - ball_radius
        ball_velocity = 0

    # ----------------- DRAWING -----------------

    screen.fill(BLACK)
    pygame.draw.circle(screen, RED, (ball_x, int(ball_y)), ball_radius)
    pygame.display.flip()
    clock.tick(100)
