import pygame

pygame.init()

clock = pygame.time.Clock()

#Camera
WORLD_HEIGHT = 1000
WORLD_WIDTH = 2000
scroll_x = 0
scroll_y = 0

text = pygame.font.Font("assets/fonts/pokemon-emerald.ttf", 29)

#Character 
player = pygame.Rect(640, 360, 66, 66)
cat = pygame.image.load("assets/mewo.webp")
cat = pygame.transform.scale(cat, (cat.get_width()/4.5, cat.get_height()/4.5))
player_spd = 5

#Obstacles

Obstacles = [
    # Map borders
    pygame.Rect(-20, 0, 20, WORLD_HEIGHT),           # Left wall
    pygame.Rect(WORLD_WIDTH, 0, 20, WORLD_HEIGHT),    # Right wall
    pygame.Rect(0, -20, WORLD_WIDTH, 20),             # Top wall
    pygame.Rect(0, WORLD_HEIGHT, WORLD_WIDTH, 20),    # Bottom wall
    # Inner obstacles
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
    mouse_pos = pygame.mouse.get_pos()
    cx, cy = mouse_pos
    player_scroll  = pygame.Rect(player.x - scroll_x, player.y - scroll_y, player.width, player.height)
    pygame.draw.rect(screen, (255, 0, 0), player_scroll)
    
    text_vel = text.render(f"X: {cx}, Y: {cy}", True,(255, 255, 255))
    #screen.blit(text_vel, (100, 50))

    mouse_offset_x = (cx - screen.get_width() / 2) * 0.5
    mouse_offset_y = (cy - screen.get_height() / 2) * 0.5
    scroll_x += (player.x - scroll_x - screen.get_width()/2 + player.width/2 + (mouse_offset_x/2)) / 15
    scroll_y += (player.y - scroll_y - screen.get_height()/2 + player.height/2 + (mouse_offset_y/2)) / 15
    screen.blit(cat, (player_scroll.x - 8, player_scroll.y - 8))

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
        pygame.draw.rect(screen, (0, 255, 255), (obs.x - scroll_x, obs.y - scroll_y, obs.width, obs.height))
           
    clock.tick(60)
    pygame.display.update()


pygame.quit()