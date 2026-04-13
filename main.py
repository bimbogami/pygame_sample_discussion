from numpy import random
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 700))
pygame.display.set_caption("sample")


# Player
player_x = 370
player_y = 320

r = 255
g = 0
b = 255


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_y -= 10
            if event.key == pygame.K_DOWN:
                player_y += 10
            if event.key == pygame.K_LEFT:
                player_x -= 10
            if event.key == pygame.K_RIGHT:
                player_x += 10
            if event.key == pygame.K_SPACE:
               r = random.randint(0, 255)
               g = random.randint(0, 255)
               b = random.randint(0, 255)

    pygame.key.set_repeat(10)
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (r, g, b), (player_x, player_y, 60, 60))
    pygame.display.flip()
pygame.quit()