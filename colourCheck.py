import pygame

# Initialize Pygame
pygame.init()

# Set up canvas
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hex Color Test")

# Function to convert hex → RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Example colors
color1 = hex_to_rgb("#FF5850")  # orange
color2 = hex_to_rgb("#00FF00")  # green
color3 = hex_to_rgb("#0000FF")  # blue

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill background black
    screen.fill((0, 0, 0))

    # Draw circles with hex colors
    pygame.draw.circle(screen, color1, (100, 150), 40)
    pygame.draw.circle(screen, color2, (200, 150), 40)
    pygame.draw.circle(screen, color3, (300, 150), 40)

    # Update screen
    pygame.display.flip()

pygame.quit()
