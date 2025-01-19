import pygame
import random
import numpy as np
import math

# Constants
units = 80
SCREEN_SIZE = 1600

GRID_SIZE = units
CELL_SIZE = 10
MAX_Z = units
MAX_W = units
FPS = 15
render = 1

# Initialize Pygame
if render:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("4D TRON Game with AI")
    clock = pygame.time.Clock()

# Colors
def gradient_color(z, w, player=1):
    intensity = max(0, min(1, (MAX_Z - z + 1) / MAX_Z))  # Clamp between 0 and 1
    if player == 1:
        return (
            int(min(255, max(0, 255 * intensity))), 
            int(min(255, max(0, 100 * intensity))), 
            int(min(255, max(0, 50 * intensity)))
        )
    else:
        return (
            int(min(255, max(0, 50 * intensity))), 
            int(min(255, max(0, 100 * intensity))), 
            int(min(255, max(0, 255 * intensity)))
        )

def draw_polygon(surface, x, y, size, color, sides):
    points = []
    angle_step = 360 / sides
    for i in range(sides):
        angle = math.radians(i * angle_step)
        px = x + size * math.cos(angle)
        py = y + size * math.sin(angle)
        points.append((px, py))
    pygame.draw.polygon(surface, color, points)

# Player Class
class Player4D:
    def __init__(self, start_pos, direction, color_func, is_ai=False):
        self.body = [start_pos]
        self.direction = direction
        self.alive = True
        self.color_func = color_func
        self.is_ai = is_ai

    def move(self, all_trails):
        if not self.alive:
            return
        head = self.body[0]
        new_head = tuple(map(sum, zip(head, self.direction)))

        if new_head in all_trails or not self.is_within_bounds(new_head):
            self.alive = False
        else:
            self.body.insert(0, new_head)

    def is_within_bounds(self, pos):
        x, y, z, w = pos
        return (
            -GRID_SIZE <= x < GRID_SIZE and
            -GRID_SIZE <= y < GRID_SIZE and
            0 <= z <= MAX_Z and
            0 <= w <= MAX_W
        )

    def change_direction(self, new_direction):
        if self.alive:
            self.direction = new_direction

# Simple AI for Players
def simple_ai(player, all_trails):
    if not player.alive:
        return

    directions = [
        (1, 0, 0, 0), (-1, 0, 0, 0), (0, 1, 0, 0), (0, -1, 0, 0),
        (0, 0, 1, 0), (0, 0, -1, 0), (0, 0, 0, 1), (0, 0, 0, -1)
    ]
    random.shuffle(directions)
    head = player.body[0]

    for d in directions:
        new_pos = tuple(map(sum, zip(head, d)))
        if new_pos not in all_trails and player.is_within_bounds(new_pos):
            player.change_direction(d)
            return

# Draw the players
def draw_players(players):
    screen.fill((0, 0, 0))
    segments = []

    for player in players:
        for idx, (x, y, z, w) in enumerate(player.body):
            segments.append((x, y, z, w, player.color_func))

    segments.sort(key=lambda segment: segment[2])

    for x, y, z, w, color_func in segments:
        draw_segment(x, y, z, w, color_func)

    pygame.display.flip()

def draw_segment(x, y, z, w, color_func):
    size = CELL_SIZE * ((MAX_Z - z + 1) / MAX_Z)
    color = color_func(z, w)
    sides = max(3, (MAX_W//3 - w//3) + 3)

    screen_x = SCREEN_SIZE // 2 + x * CELL_SIZE
    screen_y = SCREEN_SIZE // 2 + y * CELL_SIZE

    draw_polygon(screen, screen_x, screen_y, size, color, sides)

# Mode Selection
def select_mode():
    print("Select Mode:")
    #print("1. Player vs Player (PVP)")
    print("Player vs Non-Player (P V NP)")
    mode =  2 #input("Enter 1 or 2: ")
    return mode

mode = select_mode()
is_pvp = mode == '1'

print('Player 1 Controls:')

print('   Up      - W')
print('   Down    - S')
print('   Left    - A')
print('   Right   - D')
print('   Forward - Q (further)')
print('   Back    - E (closer)')
print('   Skew+   - R  (less sides)')
print('   Skew-   - F  (more sides)')
if is_pvp:
    print('Player 2 Controls:')

    print('   Up      - Up')
    print('   Down    - Down')
    print('   Left    - Left')
    print('   Right   - Right')
    print('   Forward - 8')
    print('   Back    - 2')
    print('   Skew+   - 4')
    print('   Skew-   - 6')
    
    

# Game Initialization
player1 = Player4D((0, 0, 0, 0), (1, 0, 0, 0), lambda z, w: gradient_color(z, w, player=1), is_ai=False)
player2 = Player4D((4, 4, 0, 0), (-1, 0, 0, 0), lambda z, w: gradient_color(z, w, player=2), is_ai=not is_pvp)
players = [player1, player2]

running = True

# Game Loop
while running:
    if render:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Player 1 controls
                if event.key == pygame.K_w:  # Up
                    player1.change_direction((0, -1, 0, 0))
                elif event.key == pygame.K_s:  # Down
                    player1.change_direction((0, 1, 0, 0))
                elif event.key == pygame.K_a:  # Left
                    player1.change_direction((-1, 0, 0, 0))
                elif event.key == pygame.K_d:  # Right
                    player1.change_direction((1, 0, 0, 0))
                elif event.key == pygame.K_q:  # Forward (z-axis)
                    player1.change_direction((0, 0, 1, 0))
                elif event.key == pygame.K_e:  # Backward (z-axis)
                    player1.change_direction((0, 0, -1, 0))
                elif event.key == pygame.K_r:  # Increase w
                    player1.change_direction((0, 0, 0, 1))
                elif event.key == pygame.K_f:  # Decrease w
                    player1.change_direction((0, 0, 0, -1))

                # Player 2 controls (if PVP mode)
                if is_pvp:
                    if event.key == pygame.K_UP:  # Up
                        player2.change_direction((0, -1, 0, 0))
                    elif event.key == pygame.K_DOWN:  # Down
                        player2.change_direction((0, 1, 0, 0))
                    elif event.key == pygame.K_LEFT:  # Left
                        player2.change_direction((-1, 0, 0, 0))
                    elif event.key == pygame.K_RIGHT:  # Right
                        player2.change_direction((1, 0, 0, 0))
                    elif event.key == pygame.K_KP8:  # Forward (z-axis)
                        player2.change_direction((0, 0, 1, 0))
                    elif event.key == pygame.K_KP2:  # Backward (z-axis)
                        player2.change_direction((0, 0, -1, 0))
                    elif event.key == pygame.K_KP4:  # Increase w
                        player2.change_direction((0, 0, 0, 1))
                    elif event.key == pygame.K_KP6:  # Decrease w
                        player2.change_direction((0, 0, 0, -1))

    all_trails = set()
    for player in players:
        all_trails.update(player.body)

    for player in players:
        if player.is_ai:
            simple_ai(player, all_trails)

    for player in players:
        player.move(all_trails)

    if not all(player.alive for player in players):
        running = False

    if render:
        draw_players(players)
        clock.tick(FPS)

if render:
    pygame.quit()
