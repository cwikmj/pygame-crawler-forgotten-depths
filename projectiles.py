import pygame
import math
from settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.images = {angle: [pygame.transform.scale(pygame.image.load(f'assets/spells/fireball/{angle} ({i}).png').convert_alpha(), (TEXTURE_SIZE, TEXTURE_SIZE)) for i in range(1, 9)] for angle in ["up", "down", "left", "leftdown", "leftup", "right", "rightdown", "rightup"]}
        self.image_sets = {-math.pi / 2: 'up', -math.pi / 4: 'rightup', 0: 'right', math.pi: 'left', math.pi * .75: 'leftdown', -math.pi * .75: 'leftup', math.pi / 2: 'down', math.pi / 4: 'rightdown'}
        self.blast_images = [pygame.transform.scale(pygame.image.load(f'assets/spells/blast/blast ({i}).png').convert_alpha(), (TEXTURE_SIZE, TEXTURE_SIZE)) for i in range(1, 7)]
        self.animation_delay = 50
        self.current_frame = 0
        self.last_update = 0
        self.collided = False
        self.exploded = False
        self.image = self.images[self.image_sets[direction]][self.current_frame]
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 8
        self.direction = self.image_sets[direction]
        self.velocity = pygame.Vector2(self.speed * math.cos(direction), self.speed * math.sin(direction))

    def update(self):
        if not self.collided:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.animation_delay:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.images[self.direction])
                self.image = self.images[self.direction][self.current_frame]
            self.rect.move_ip(self.velocity.x, self.velocity.y)
        else:
            if self.current_frame >= len(self.blast_images):
                self.current_frame = 0
            now = pygame.time.get_ticks()
            if not self.exploded and now - self.last_update > self.animation_delay:
                self.last_update = now
                self.image = self.blast_images[self.current_frame]
                self.current_frame += 1
                if self.current_frame >= len(self.blast_images):
                    self.current_frame = 0
                    self.exploded = True

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_wall_collision(self, map):
        for y in range(
            max(0, map.y_offset // TEXTURE_SIZE),
            min(len(map.maze), (map.y_offset + HEIGHT) // TEXTURE_SIZE + 1)
        ):
            for x in range(
                max(0, map.x_offset // TEXTURE_SIZE),
                min(len(map.maze[0]), (map.x_offset + WIDTH) // TEXTURE_SIZE + 1)
            ):
                if map.maze[y][x][3]:
                    tile_rect = pygame.Rect(x * TEXTURE_SIZE - map.x_offset, y * TEXTURE_SIZE - map.y_offset, TEXTURE_SIZE, TEXTURE_SIZE)
                    if self.rect.colliderect(tile_rect):
                        return True
        return False