import pygame
from settings import *
from levels import *
from player import *
from sounds import *

class Map:
    def __init__(self, x, y):
        self.x_offset = x
        self.y_offset = y
        self.maze = [[
            [i, j, dungeon_map[i][j], True] if dungeon_map[i][j] in dungeon_wall_tiles else [i, j, dungeon_map[i][j], False]
            for j in range(2 * WIDTH // TEXTURE_SIZE)] for i in range(2 * HEIGHT // TEXTURE_SIZE)]
        self.map_tiles = [pygame.transform.scale(pygame.image.load(f'assets/map/({i}).png').convert_alpha(), (TEXTURE_SIZE, TEXTURE_SIZE)) for i in range(1, 161)]
        self.dungeon_wall_tiles = dungeon_wall_tiles
        self.decoration_tiles = []
        self.complete = False

    def update_maze(self, screen):
        visible_rows = range(max(0, self.y_offset // TEXTURE_SIZE), min(len(self.maze), (self.y_offset + HEIGHT) // TEXTURE_SIZE + 1))
        visible_cols = range(max(0, self.x_offset // TEXTURE_SIZE), min(len(self.maze[0]), (self.x_offset + WIDTH) // TEXTURE_SIZE + 1))

        for y in visible_rows:
            for x in visible_cols:
                rect = pygame.Rect(x * TEXTURE_SIZE - self.x_offset, y * TEXTURE_SIZE - self.y_offset, TEXTURE_SIZE, TEXTURE_SIZE)
                dungeon_tile = self.map_tiles[self.maze[y][x][2] - 1]
                screen.blit(dungeon_tile, rect)

                if dungeon_decoration[y][x] != -1:
                    decor_tile = self.map_tiles[dungeon_decoration[y][x] - 1]
                    screen.blit(decor_tile, rect)

    def check_if_wall(self, y, x):
        return self.maze[y][x][3]

class Chest(pygame.sprite.Sprite):
    def __init__(self, pickup, cap, item, qty=1):
        super().__init__()
        self.x = pickup[0]
        self.y = pickup[1]
        self.cap = cap
        self.item = item
        self.qty = qty
        self.opened = False
        self.sound = Sounds()

    def check_proximity(self, player, map):
        player_x, player_y = player.rect.x // TEXTURE_SIZE, player.rect.y // TEXTURE_SIZE
        if abs(player_x - self.x) <= 0.5 and abs(player_y - self.y) <= 0.5:
            if not self.opened:
                self.opened = True
                dungeon_decoration[self.cap[1]][self.cap[0]] = 70
                dungeon_decoration[self.cap[1] + 1][self.cap[0]] = 79
                self.sound.load_sound(sound_paths['key_found'])
                self.sound.play_sound()
                if self.item != 'key':
                    player.stats.__dict__[f"{self.item}_potions"] += self.qty
                else:
                    player.stats.keys += 1

        elif abs(player_x - 45) <= 0.5 and abs(player_y - 27) <= 0.5 and player.stats.keys > 0:
            player.stats.keys = 0
            self.sound.load_sound(sound_paths['final_door_open'])
            self.sound.play_sound()
            dungeon_decoration[25][45:48] = [122, 143, 124]
            dungeon_decoration[26][45:48] = [131, 152, 133]
            dungeon_decoration[27][45:48] = [140, 141, 142]
            map.complete = True

# Use a single surface for rendering the maze: Instead of creating a new surface for each wall tile, you can create 
# a single surface to render the entire maze. This will reduce the number of blit operations and improve performance.

# Only update visible portions of the maze: Instead of updating the entire maze on each frame, you can calculate 
# the visible portion of the maze based on the player's position and only update that portion. This will reduce the amount
# of rendering required and improve performance.

# Cache the wall tile images: Instead of loading the wall tile image from disk on each frame, you can load the images
# once and cache them for reuse. This will reduce disk I/O and improve performance.