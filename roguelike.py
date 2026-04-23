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

    print(f"[{lvl['name']}] loaded — {len(lvl['obstacles'])} obstacles")
    return world_w, world_h, obstacles, lvl["name"]

WORLD_WIDTH, WORLD_HEIGHT, Obstacles, level_name = load_level(current_level_index)

# ── Camera ────────────────────────────────────────────────────────────────────
scroll_x = 0
scroll_y = 0

# ── Assets ────────────────────────────────────────────────────────────────────
text_font = pygame.font.Font("assets/fonts/pokemon-emerald.ttf", 29)
hud_font  = pygame.font.Font("assets/fonts/pokemon-emerald.ttf", 22)

# ── Player ────────────────────────────────────────────────────────────────────
player = pygame.Rect(640, 360, 66, 66)
cat = pygame.image.load("assets/mewo.webp")
cat = pygame.transform.scale(cat, (cat.get_width() / 4.5, cat.get_height() / 4.5))
player_spd = 5

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
                WORLD_WIDTH, WORLD_HEIGHT, Obstacles, level_name = load_level(current_level_index)
                player.topleft = (640, 360)
                scroll_x, scroll_y = 0, 0

            if event.key == pygame.K_b:
                current_level_index = (current_level_index - 1) % TOTAL_LEVELS
                WORLD_WIDTH, WORLD_HEIGHT, Obstacles, level_name = load_level(current_level_index)
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

    # ── Player movement + collision ───────────────────────────────────────────
    player.x += (keys[pygame.K_RIGHT] or keys[pygame.K_d]) * player_spd \
              - (keys[pygame.K_LEFT]  or keys[pygame.K_a]) * player_spd
    for obs in Obstacles:
        if player.colliderect(obs):
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
                player.right = obs.left
            if (keys[pygame.K_LEFT]  or keys[pygame.K_a]):
                player.left  = obs.right

    player.y += (keys[pygame.K_DOWN] or keys[pygame.K_s]) * player_spd \
              - (keys[pygame.K_UP]   or keys[pygame.K_w]) * player_spd
    for obs in Obstacles:
        if player.colliderect(obs):
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
                player.bottom = obs.top
            if (keys[pygame.K_UP]   or keys[pygame.K_w]):
                player.top    = obs.bottom

    # ── Draw obstacles ────────────────────────────────────────────────────────
    for obs in Obstacles:
        pygame.draw.rect(screen, (0, 255, 255),
                         (obs.x - scroll_x, obs.y - scroll_y, obs.width, obs.height))

    # ── Draw player ───────────────────────────────────────────────────────────
    player_scroll = pygame.Rect(player.x - scroll_x, player.y - scroll_y,
                                player.width, player.height)
    pygame.draw.rect(screen, (255, 0, 0), player_scroll)
    screen.blit(cat, (player_scroll.x - 8, player_scroll.y - 8))

    # ── HUD ───────────────────────────────────────────────────────────────────
    level_surf = text_font.render(
        f"{level_name}  ({current_level_index + 1}/{TOTAL_LEVELS})  N - Next  B - Back",
        True, (255, 255, 200)
    )
    screen.blit(level_surf, (10, 10))

    clock.tick(60)
    pygame.display.update()

pygame.quit()