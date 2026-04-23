import pygame

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

text = pygame.font.Font("assets/fonts/pokemon-emerald.ttf", 29)

# Hide default mouse
pygame.mouse.set_visible(False)

# Define a button rect for hover testing
button_rect = pygame.Rect(300, 250, 200, 50)
color_default = (0, 128, 255)
color_hover = (0, 200, 255)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))
    mouse_pos = pygame.mouse.get_pos()
    cx, cy = mouse_pos
    text_vel = text.render(f"X: {cx}, Y: {cy}", True,(255, 255, 255))


    screen.blit(text_vel, (100, 50))

    # 1. --- Hover Detection ---
    if button_rect.collidepoint(mouse_pos):
        current_color = color_hover
    else:
        current_color = color_default
    
    # Draw Button
    pygame.draw.rect(screen, current_color, button_rect)

    # 2. --- Crosshair Drawing ---
    # Draw a simple crosshair (lines)
    cx, cy = mouse_pos
    pygame.draw.line(screen, (255, 0, 0), (cx - 10, cy), (cx + 10, cy), 2)
    pygame.draw.line(screen, (255, 0, 0), (cx, cy - 10), (cx, cy + 10), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
