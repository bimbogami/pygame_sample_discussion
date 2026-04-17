import pygame
import sys

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load and resize background image
bg = pygame.image.load('assets/bg.jpg').convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Background scroll variables
bg_x = 0
bg_speed = 5

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update background position
    bg_x -= bg_speed
    
    # Reset position for infinite scroll
    if bg_x <= -WIDTH:
        bg_x = 0

    # Draw backgrounds
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + WIDTH, 0)) # Secondary image

    pygame.display.flip()
    clock.tick(60)
