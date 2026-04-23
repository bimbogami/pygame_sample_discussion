import pygame

pygame.init()

clock = pygame.time.Clock()

#Character 
player = pygame.Rect(640, 360, 66, 66)
cat = pygame.image.load("assets/mewo.webp")
cat = pygame.transform.scale(cat, (cat.get_width()/4.5, cat.get_height()/4.5))
player_spd = 5

#Obstacles

Obstacles = [
    pygame.Rect(200, 150, 400, 20),
    pygame.Rect(300, 200, 50, 200)
]

#Screen
screen = pygame.display.set_mode((1280,720))

run = True

while run:
    
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("SHOOT")
            
    keys = pygame.key.get_pressed()


    player.x += (keys[pygame.K_RIGHT] or keys[pygame.K_d]) * player_spd - (keys[pygame.K_LEFT] or keys[pygame.K_a]) * player_spd
    for obs in Obstacles:
        if player.colliderect(obs):
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
                player.right = obs.left
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
                player.left = obs.right

    player.y += (keys[pygame.K_DOWN] or keys[pygame.K_s]) * player_spd - (keys[pygame.K_UP] or keys[pygame.K_w]) * player_spd
    for obs in Obstacles:
        if player.colliderect(obs):
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
                player.bottom = obs.top
            if (keys[pygame.K_UP] or keys[pygame.K_w]):
                player.top = obs.bottom

    for obs in Obstacles:
        pygame.draw.rect(screen, (0, 255, 255), obs)
           
    clock.tick(60)
    pygame.draw.rect(screen, (255, 0, 0), player)
    screen.blit(cat, (player.x - 8, player.y - 8))
    pygame.display.update()


pygame.quit()