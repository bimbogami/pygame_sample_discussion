import pygame
import json

pygame.init()

clock = pygame.time.Clock()

# Load level data from JSON
with open("levels.json", "r") as f:
    level_data = json.load(f)

# ── Level loader ─────────────────────────────────────────────────────────────
current_level_index = 0

def load_level(index):
    """Load level by index and return (world_w, world_h, Obstacles list)."""
    lvl = level_data["levels"][index]
    world_w = lvl["world_width"]
    world_h = lvl["world_height"]


    obstacles = [
        # Border walls
        pygame.Rect(-20, 0, 20, world_h),           # Left wall
        pygame.Rect(world_w, 0, 20, world_h),        # Right wall
        pygame.Rect(0, -20, world_w, 20),            # Top wall
        pygame.Rect(0, world_h, world_w, 20),        # Bottom wall
    ]
    for obs in lvl["obstacles"]:
        obstacles.append(pygame.Rect(obs["x"], obs["y"], obs["w"], obs["h"]))

    print(f"[{lvl['name']}] loaded — {len(lvl['obstacles'])} obstacles texture: {lvl['walls']}")
    return world_w, world_h, obstacles, lvl["name"], lvl["walls"]

WORLD_WIDTH, WORLD_HEIGHT, Obstacles, level_name, texture = load_level(current_level_index)

# ── Camera ────────────────────────────────────────────────────────────────────
scroll_x = 0
scroll_y = 0

# ── Assets ────────────────────────────────────────────────────────────────────
text_font = pygame.font.Font("assets/fonts/pokemon-emerald.ttf", 29)
hud_font  = pygame.font.Font("assets/fonts/pokemon-emerald.ttf", 22)

# ── Player ────────────────────────────────────────────────────────────────────
player = pygame.Rect(640, 360, 66, 66)
portal = pygame.Rect(1200, 700, 66, 66)
cat = pygame.image.load("assets/mewo.webp")
cat = pygame.transform.scale(cat, (cat.get_width() / 4.5, cat.get_height() / 4.5))
player_spd = 5
flip = False  # initialized once; updated each frame based on mouse side

# ── Screen ────────────────────────────────────────────────────────────────────
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Roguelike")

TOTAL_LEVELS = len(level_data["levels"])

# ── Main loop ─────────────────────────────────────────────────────────────────
run = True

while run:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("SHOOT")

            # ── Level switching: N = next, B = back ──────────────────────────
            if event.key == pygame.K_n:
                current_level_index = (current_level_index + 1) % TOTAL_LEVELS
                WORLD_WIDTH, WORLD_HEIGHT, Obstacles, level_name, texture = load_level(current_level_index)
                player.topleft = (640, 360)
                scroll_x, scroll_y = 0, 0

            if event.key == pygame.K_b:
                current_level_index = (current_level_index - 1) % TOTAL_LEVELS
                WORLD_WIDTH, WORLD_HEIGHT, Obstacles, level_name, texture = load_level(current_level_index)
                player.topleft = (640, 360)
                scroll_x, scroll_y = 0, 0

    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    cx, cy = mouse_pos

    # ── Camera scroll ─────────────────────────────────────────────────────────
    mouse_offset_x = (cx - screen.get_width()  / 2) * 0.5
    mouse_offset_y = (cy - screen.get_height() / 2) * 0.5
    scroll_x += (player.x - scroll_x - screen.get_width()  / 2 + player.width  / 2 + mouse_offset_x / 2) / 15
    scroll_y += (player.y - scroll_y - screen.get_height() / 2 + player.height / 2 + mouse_offset_y / 2) / 15

    # ─── Player Facing ─────────────────────────────────────────────────────────
    if cx < screen.get_width()/2:
        flip = True
        
    elif cx > screen.get_width()/2:
        flip = False
    
    

    # ── Player movement + collision ───────────────────────────────────────────
    old_x = player.x
    player.x += (keys[pygame.K_RIGHT] or keys[pygame.K_d]) * player_spd \
              - (keys[pygame.K_LEFT]  or keys[pygame.K_a]) * player_spd
    for obs in Obstacles:
        if player.colliderect(obs):
            if player.x > old_x:    # actually moved right
                player.right = obs.left
            elif player.x < old_x:  # actually moved left
                player.left  = obs.right

    old_y = player.y
    player.y += (keys[pygame.K_DOWN] or keys[pygame.K_s]) * player_spd \
              - (keys[pygame.K_UP]   or keys[pygame.K_w]) * player_spd
    for obs in Obstacles:
        if player.colliderect(obs):
            if player.y > old_y:    # actually moved down
                player.bottom = obs.top
            elif player.y < old_y:  # actually moved up
                player.top    = obs.bottom

    # ── Draw obstacles ────────────────────────────────────────────────────────
    tile_img = pygame.image.load(f"assets/tiles/{texture}.png").convert()
    tile_img = pygame.transform.scale(tile_img, (tile_img.get_width()*4, tile_img.get_height()*4))
    tile_img.set_alpha(255)  # 0 = invisible, 255 = fully opaque
    for obs in Obstacles:
        pygame.draw.rect(screen, (255,255,0), (obs.x - scroll_x, obs.y - scroll_y, obs.width, obs.height))
        # Clip drawing to the obstacle bounds so tiles don't bleed outside
        screen.set_clip(pygame.Rect(obs.x - scroll_x, obs.y - scroll_y, obs.width, obs.height))
        for tx in range(obs.x, obs.x + obs.width, tile_img.get_width()):
            for ty in range(obs.y, obs.y + obs.height, tile_img.get_height()):
                screen.blit(tile_img, (tx - scroll_x, ty - scroll_y))
        screen.set_clip(None)  # restore full-screen drawing

    # ── Draw player ───────────────────────────────────────────────────────────
    player_scroll = pygame.Rect(player.x - scroll_x, player.y - scroll_y, player.width, player.height)
    pygame.draw.rect(screen, (255, 0, 0), player_scroll)
    cat_image = pygame.transform.flip(cat, flip, False)
    screen.blit(cat_image, (player_scroll.x - 8, player_scroll.y - 8))  

    # ── Draw player ───────────────────────────────────────────────────────────
    pygame.draw.rect(screen, (234, 34, 100), (portal.x - scroll_x, portal.y - scroll_y, portal.width, portal.height))
    if player.colliderect(portal):
        current_level_index = (current_level_index + 1) % TOTAL_LEVELS
        WORLD_WIDTH, WORLD_HEIGHT, Obstacles, level_name, texture = load_level(current_level_index)
        player.topleft = (640, 360)
        scroll_x, scroll_y = 0, 0
    # ── HUD ───────────────────────────────────────────────────────────────────
    level_surf = text_font.render(
        f"{level_name}  ({current_level_index + 1}/{TOTAL_LEVELS})  N - Next  B - Back",
        True, (255, 255, 200)
    )
    screen.blit(level_surf, (10, 10))

    clock.tick(60)
    pygame.display.update()

pygame.quit()