import pygame
import random
import sys

# --- Ustawienia ---
CELL_SIZE = 32
SCORE = 0
CURRENT_GOAL= 1
CURRENT_POINTS =0
GRID_WIDTH = 32
GRID_HEIGHT = 32
WINDOW_SIZE = (GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE)

TRAIN_SPEED = 3  # pól na sekundę
DRAW_FPS = 1# 1 klatka na sekundę
MOVE_DELAY = 1000 // TRAIN_SPEED  # ms

# --- Inicjalizacja ---
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

TILE_SIZE = CELL_SIZE
train_img = pygame.image.load(".venv/assets/train.png")
train_img = pygame.transform.scale(train_img, (TILE_SIZE, TILE_SIZE))
train_images = {
    'up':pygame.transform.rotate(train_img,90),
    'down':pygame.transform.rotate(train_img,-90),
    'right':train_img,
    'left':pygame.transform.rotate(train_img,180)
}


track_img = pygame.image.load(".venv/assets/track.png")
track_img = pygame.transform.scale(track_img, (TILE_SIZE, TILE_SIZE))

curve_img = pygame.image.load(".venv/assets/curve.png")
curve_img = pygame.transform.scale(curve_img, (TILE_SIZE, TILE_SIZE))
track_images = {
    ('straight', 'vertical'): track_img,#pygame.image.load(".venv/assets/track.png"),
    ('straight', 'horizontal'): pygame.transform.rotate(track_img,90),#pygame.image.load(".venv/assets/track.png"), 90),

    ('curve', 'up-right'): pygame.transform.rotate(curve_img,0),
    ('curve', 'right-down'): pygame.transform.rotate(curve_img,270),
    ('curve', 'down-left'): pygame.transform.rotate(curve_img,180),
    ('curve', 'left-up'): pygame.transform.rotate(curve_img,90)
}

man_imgs = [
pygame.transform.scale(pygame.image.load(".venv/assets/guy1.png"),(TILE_SIZE, TILE_SIZE)),
pygame.transform.scale(pygame.image.load(".venv/assets/guy2.png"),(TILE_SIZE, TILE_SIZE)),
pygame.transform.scale(pygame.image.load(".venv/assets/guy3.png"),(TILE_SIZE, TILE_SIZE)),
pygame.transform.scale(pygame.image.load(".venv/assets/guy4.png"),(TILE_SIZE, TILE_SIZE)),
]
# --- Stan gry ---
train = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
direction = (1, 0)
tracks = {}
trains = {}
goal = {((random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)),0)}

# Timery
last_move = pygame.time.get_ticks()
last_draw = pygame.time.get_ticks()
prev_direction = direction
def move_train():
    global train, tracks, prev_direction, SCORE
    score = SCORE
    head_x, head_y = train[-1]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    # Kolizje
    if (
        new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
        new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
        new_head in tracks
    ):

        print("Game Over!\nYour score:", SCORE)
        game_over_screen()
        pygame.quit()
        sys.exit()

    track_type, track_dir = get_track_type(prev_direction, direction)
    tracks[(head_x, head_y)] = (track_type, track_dir)
    train_type = get_train_type(direction)
    train.append(new_head)
    prev_direction = direction
    #tracks.add((head_x, head_y))

    # Sprawdź cel
    #for f in goal:
    if goal.__contains__((new_head,0))or goal.__contains__((new_head,1)) or goal.__contains__((new_head,2)) or goal.__contains__((new_head,3)):
        #if f[0] == new_head:
        global CURRENT_GOAL, CURRENT_POINTS
        SCORE += 1
        CURRENT_POINTS += 1
        if CURRENT_POINTS >= CURRENT_GOAL:
            goal.clear()
            tracks.clear()
            CURRENT_GOAL += 1
            CURRENT_POINTS = 0
            for i in range(0,CURRENT_GOAL):
                place_new_goal()

    else:
        train.pop(0)  # porusza się jak wąż

def get_track_type(prev_dir, curr_dir):
    if prev_dir == curr_dir:
        if curr_dir in [(1, 0), (-1, 0)]:
            return 'straight', 'horizontal'
        else:
            return 'straight', 'vertical'
    else:
        # Zakręty
        turns = {
            ((0, -1), (1, 0)): ('curve', 'down-left'),
            ((1, 0), (0, 1)): ('curve', 'left-up'),
            ((0, 1), (-1, 0)): ('curve', 'up-right'),
            ((-1, 0), (0, -1)): ('curve', 'right-down'),

            ((0, -1), (-1, 0)): ('curve', 'left-up'),#UL
            ((-1, 0), (0, 1)): ('curve', 'down-left'),#LD
            ((0, 1), (1, 0)): ('curve', 'right-down'),#DR
            ((1, 0), (0, -1)): ('curve', 'up-right'),#RU
        }
        return turns.get((prev_dir, curr_dir), ('straight', 'horizontal'))  # domyślnie
def get_train_type(curr_dir):
    turns = {
        (0, 1): 'left',
        (-1, 0): 'up',
        (1, 0): 'down',
        (0, -1):'right'
    }

    return turns.get(curr_dir, 'right')
def place_new_goal():
    global goal
    a = random.randint(0, 3)
    while True:
        new_goal = ((random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)),a)
        if new_goal not in tracks:
            goal.add(new_goal)
            break

def draw():
    screen.fill((0, 0, 0))

    for (x, y), (track_type, track_dir) in tracks.items():
        img = track_images[(track_type, track_dir)]
        screen.blit(img, (x * CELL_SIZE, y * CELL_SIZE))

#    for (x, y) in tracks:
 #       screen.blit(track_img, (x * CELL_SIZE, y * CELL_SIZE))

    for (x, y) in train:
        rotated_train = train_images[get_train_type(direction)]
        head_x, head_y = train[-1]
        screen.blit(rotated_train, (head_x * TILE_SIZE, head_y * TILE_SIZE))
        #screen.blit(train_img, (x * CELL_SIZE, y * CELL_SIZE))

    # Cel
    for g in goal:
        screen.blit(man_imgs[g[1]], (g[0][0] * TILE_SIZE, g[0][1] * TILE_SIZE))

    pygame.display.flip()

def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return

def game_over_screen():
    font = pygame.font.SysFont(None, 48)

    line1 = font.render("GAME OVER", True, (255, 0, 0))
    line2 = font.render(f"YOUR SCORE: {SCORE}", True, (255, 255, 255))

    # Wyśrodkowanie
    rect1 = line1.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 - 30))
    rect2 = line2.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + 30))

    screen.fill((0, 0, 0))
    screen.blit(line1, rect1)
    screen.blit(line2, rect2)
    pygame.display.flip()



    # Czekaj na klawisz
    wait_for_key()


# --- Główna pętla ---
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Sterowanie
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: direction = (0, -1)
            elif event.key == pygame.K_DOWN: direction = (0, 1)
            elif event.key == pygame.K_LEFT: direction = (-1, 0)
            elif event.key == pygame.K_RIGHT: direction = (1, 0)

    now = pygame.time.get_ticks()

    if now - last_move >= MOVE_DELAY:
        move_train()
        last_move = now

    if now - last_draw >= 1000 // DRAW_FPS:
        draw()
        last_draw = now
        DRAW_FPS = random.randint(1, 15)/3

    clock.tick(60)
