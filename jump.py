import pygame
from numpy import random

pygame.init()

WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spanning Background Effect")
clock = pygame.time.Clock()

bg_image = pygame.image.load("assets/bg2.jpg").convert()

WORLD_WIDTH = 2000
WORLD_HEIGHT = 1000
bg_image = pygame.transform.scale(bg_image, (WORLD_WIDTH, WORLD_HEIGHT))

grav = 0.5
jump = -15
spd = 7

y_vel = 0
on_ground = True
scroll_x = 0
scroll_y = 0

player = pygame.Rect(370, 320, 50, 50)
platforms = [
    pygame.Rect(0, 600, 2000, 200),
    pygame.Rect(200, 450, 200, 50),
    pygame.Rect(600, 300, 200, 50),
    pygame.Rect(1000, 200, 300, 50)
]

r, g, b = 255, 0, 255
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            if event.key == pygame.K_UP and on_ground:
                y_vel = jump

    y_vel += grav
    player.y += y_vel
    on_ground = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= spd
    if keys[pygame.K_RIGHT]:
        player.x += spd

    for platform in platforms:
        if player.colliderect(platform):
            if y_vel > 0: 
                player.bottom = platform.top
                y_vel = 0
                on_ground = True

    scroll_x += (player.x - scroll_x - WIDTH/2 + player.width/2) / 15
    scroll_y += (player.y - scroll_y - HEIGHT/2 + player.height/2) / 15

    screen.fill((0, 0, 0))

    screen.blit(bg_image, (-scroll_x, -scroll_y))

    for platform in platforms:
        draw_rect = pygame.Rect(platform.x - scroll_x, platform.y - scroll_y, platform.width, platform.height)
        pygame.draw.rect(screen, (4, 89, 0), draw_rect)

    player_draw_rect = pygame.Rect(player.x - scroll_x, player.y - scroll_y, player.width, player.height)
    pygame.draw.rect(screen, (r, g, b), player_draw_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()