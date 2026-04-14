from numpy import random
import pygame
pygame.init()

screen = pygame.display.set_mode((800, 700))
pygame.display.set_caption("sample")
clock = pygame.time.Clock()
# Constants
grav = 0.5
jump = -15
spd = 7
y_vel = 0

# Platform 
platforms = [
    pygame.Rect(0, 600, 800, 200),
    pygame.Rect(200, 450, 200, 50)   
]

# Player

player = pygame.Rect(370, 320, 50, 50)
on_ground = True

r = 255
g = 0
b = 255


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
               r = random.randint(0, 255)
               g = random.randint(0, 255)
               b = random.randint(0, 255)
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



    #pygame.key.set_repeat(10)

    for platform in platforms:
        pygame.Rect(platform)
        if player.colliderect(platform):
            if y_vel > 0:
                player.bottom = platform.top
                y_vel = 0
                on_ground = True


    screen.fill((0, 0, 0))
    for platform in platforms:
        pygame.draw.rect(screen, (4, 89, 0), platform)
    pygame.draw.rect(screen, (r, g, b), player)
    clock.tick(60)
    pygame.display.flip()
pygame.quit()