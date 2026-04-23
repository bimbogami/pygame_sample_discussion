import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 720))

text = pygame.font.Font("assets/fonts/pokemon-emerald.ttf", 40)

# Platforms

platforms = [
    pygame.Rect(0, 600, 2000, 200),
    pygame.Rect(200, 450, 200, 50),
    pygame.Rect(600, 300, 200, 50),
    pygame.Rect(1000, 200, 300, 50),
    pygame.Rect(1500, 400, 400, 50)

]

# Camera movement
WORLD_HEIGHT = 1000
WORLD_WIDTH = 2000
scroll_x = 0
scroll_y = 0

#physics 
jump = -18
gravity = 0.8
speed = 7
y_vel = 0
on_ground = True

clock = pygame.time.Clock()

#player 
player = pygame.Rect(640, 360, 66, 66)

cat = pygame.image.load("assets/mewo.webp")
cat = pygame.transform.scale(cat, (cat.get_width()/4.5, cat.get_height()/4.5))

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and on_ground:
                y_vel += jump
                on_ground = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed
    
    y_vel += gravity
    player.y += y_vel
    
    text_vel = text.render(f"Y Vel: {y_vel}", True,(255, 255, 255))
    

    screen.fill((0, 145, 131))
    screen.blit(text_vel, (100, 50))
    #SCROLL PART
    player_scroll  = pygame.Rect(player.x - scroll_x, player.y - scroll_y, player.width, player.height)
    pygame.draw.rect(screen, (255, 0, 0), player_scroll)
    scroll_x += (player.x - scroll_x - screen.get_width()/2 + player.width/2)/15
    scroll_y += (player.y - scroll_y - screen.get_height()/2 + player.height/2)/15    
    screen.blit(cat, (player_scroll.x - 8, player_scroll.y - 8))
    for platform in platforms:
        #pygame.draw.rect(screen, (44, 173, 29), platform)
        #draw_plat = pygame.Rect
        pygame.draw.rect(screen, (65, 255, 60), (platform.x - scroll_x, platform.y - scroll_y, platform.width, platform.height))
        if player.colliderect(platform):
            if y_vel > 0:
                player.bottom = platform.top
                y_vel = 0
                on_ground = True
            if y_vel < 0:
                player.top = platform.bottom
                y_vel = 0

    clock.tick(60)
    pygame.display.update() # .flip()


pygame.quit()