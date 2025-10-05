# We import external libraries to use their functions/classes
import pygame   # pygame is a library for making games (graphics, sound, input)
import sys      # sys lets us exit the game properly

# ----------------- GAME SETUP -----------------

# Call (invoke) a function to initialize pygame library before using it
pygame.init()

# Variables for screen width and height (integers)
WIDTH, HEIGHT = 500, 500

# Function call to create a game window (object of Surface class)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Function call to set title of the window (string argument)
pygame.display.set_caption("Ball Bounce Game")

# RGB colors represented as tuples (immutable sequence of 3 integers)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)

# ----------------- BALL SETTINGS -----------------

# Integer variable for ball radius
ball_radius = 20

# Integer variables for ball position (X is middle, Y is bottom of screen)
ball_x = WIDTH // 2              # // is floor division operator
ball_y = HEIGHT - ball_radius    # subtraction operator

# Float variable for velocity of ball (0 initially)
ball_velocity = 0

# Float variable for gravity (constant value added each frame)
gravity = 0.5

# Integer variable for jump strength (negative = upward movement)
jump_strength = -10

# ----------------- CLOCK SETTINGS -----------------

# Create an object of Clock class to control FPS (frames per second)
clock = pygame.time.Clock()

# ----------------- GAME LOOP -----------------

# Infinite loop using while True → keeps game running until user exits
while True:

    # for loop iterates over a list of events returned by pygame
    for event in pygame.event.get():

        # Conditional statement (if) checks if event is of type QUIT (user closed window)
        if event.type == pygame.QUIT:
            pygame.quit()   # Function to close pygame
            sys.exit()      # Function to exit program

        # Another conditional → check if a key was pressed
        if event.type == pygame.KEYDOWN:

            # Nested conditional → check if pressed key was SPACEBAR
            # and ball is on ground (so no double jump)
            if event.key == pygame.K_SPACE and ball_y == HEIGHT - ball_radius:
                ball_velocity = jump_strength   # assignment statement changes variable value

    # ----------------- PHYSICS -----------------

    # Each frame, increase velocity by gravity (float addition)
    ball_velocity += gravity

    # Update ball's Y position by adding velocity (float + int)
    ball_y += ball_velocity

    # Conditional → if ball goes below ground, reset it
    if ball_y >= HEIGHT - ball_radius:
        ball_y = HEIGHT - ball_radius   # assign fixed value (ground position)
        ball_velocity = 0               # stop moving

    # ----------------- DRAWING -----------------

    # Function call to fill screen with white color (RGB tuple)
    screen.fill(WHITE)

    # Function call to draw a circle (red, center (x,y), radius)
    pygame.draw.circle(screen, RED, (ball_x, int(ball_y)), ball_radius)

    # Function call to update display with new drawings
    pygame.display.flip()

    # Function call to pause loop so it runs at 60 FPS
    clock.tick(60)
