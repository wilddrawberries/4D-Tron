import pygame
import random




import numpy as np
import random



while True:


    # Constants
    units=10
    SCREEN_SIZE = 800
    GRID_SIZE = units
    CELL_SIZE = 20
    MAX_Z = units
    MAX_W = units
    FPS = 50
    render=1
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

    import math  # Ensure this is at the top of your script

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
            self.body = [start_pos]  # Starting position (x, y, z, w)
            self.direction = direction  # Initial direction
            self.alive = True
            self.color_func = color_func
            self.is_ai = is_ai

        def move(self, all_trails):
            if not self.alive:
                return
            head = self.body[0]
            new_head = tuple(map(sum, zip(head, self.direction)))

            if new_head in all_trails or not self.is_within_bounds(new_head):
                self.alive = False  # Player collided with a trail or boundary
            else:
                self.body.insert(0, new_head)  # Add new head position

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
        random.shuffle(directions)  # Randomize direction priority
        head = player.body[0]

        for d in directions:
            new_pos = tuple(map(sum, zip(head, d)))
            if (
                new_pos not in all_trails and  # Avoid collisions with trails
                player.is_within_bounds(new_pos)  # Stay within bounds
            ):
                player.change_direction(d)
                return

    # Draw the players
    def draw_players(players):
        screen.fill((0, 0, 0))  # Clear screen

        # Collect all segments with their z-coordinates
        segments = []
        for player in players:
            for idx, (x, y, z, w) in enumerate(player.body):
                segments.append((x, y, z, w, player.color_func))

        # Sort segments based on z-coordinate (closer to screen first)
        segments.sort(key=lambda segment: segment[2])

        # Draw segments in sorted order
        for x, y, z, w, color_func in segments:
            draw_segment(x, y, z, w, color_func)

        pygame.display.flip()

    def draw_segment(x, y, z, w, color_func):
        size = CELL_SIZE * ((MAX_Z - z + 1) / MAX_Z)  # Adjust size based on Z
        color = color_func(z, w)
        sides = max(3, MAX_W - w + 3)  # W determines polygon sides

        screen_x = SCREEN_SIZE // 2 + x * CELL_SIZE
        screen_y = SCREEN_SIZE // 2 + y * CELL_SIZE

        draw_polygon(screen, screen_x, screen_y, size, color, sides)
    # Game IniX tialization
    player1 = Player4D((0, 0, 0, 0), (1, 0, 0, 0), lambda z, w: gradient_color(z, w, player=1), is_ai=True)
    player2 = Player4D((4, 4, 0, 0), (-1, 0, 0, 0), lambda z, w: gradient_color(z, w, player=2), is_ai=True)
    players = [player1, player2]

    running = 1

    # Game Loop
    while running:
        if render:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        # Collect all trails for collision detection
        all_trails = set()
        
        for player in players:
            all_trails.update(player.body)

        # AI Movement
        for player in players:
            if player.is_ai:
                simple_ai(player, all_trails)

        # Move players
        for player in players:
            player.move(all_trails)

        # Check if any player is not alive
        if not all(player.alive for player in players):
            running = False
        if render:
            draw_players(players)

            clock.tick(FPS)

    if render:
        pygame.quit()
    running=0
        

