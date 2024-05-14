import pygame
import math
from settings import *
from map import *
from player import *
from sounds import *
from playerstats import *
from pathfinding import *

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        self.action_images = {}
        directions = ['up', 'down', 'left', 'right']
        for direction in directions:
            self.action_images[f'walk_{direction}'] = [pygame.image.load(f'assets/sprites/{self.type}/walk/{direction} ({i}).png').convert_alpha() for i in range(1, 9)]
            self.action_images[f'attack_{direction}'] = [pygame.image.load(f'assets/sprites/{self.type}/attack/{direction} ({i}).png').convert_alpha() for i in range(1, 7)] if type == 'SKELETON' else [pygame.image.load(f'assets/sprites/{self.type}/attack/{direction} ({i}).png').convert_alpha() for i in range(1, 8)]
            self.action_images[f'idle_{direction}'] = [pygame.image.load(f'assets/sprites/{self.type}/idle/{direction}.png').convert_alpha()] if type == 'SKELETON' else [pygame.image.load(f'assets/sprites/{self.type}/idle/{direction} ({i}).png').convert_alpha() for i in range(1, 8)]
        self.action_images['death'] = [pygame.image.load(f'assets/sprites/{self.type}/death/death ({i}).png').convert_alpha() for i in range(1, 7)] if type == 'SKELETON' else [pygame.image.load(f'assets/sprites/{self.type}/death/death ({i}).png').convert_alpha() for i in range(1, 10)]
        self.action_images_scaled = {
            action: [pygame.transform.scale(image, (NPC_STATS[self.type]["SIZE"], NPC_STATS[self.type]["SIZE"])) for image in images]
            for action, images in self.action_images.items()
        }
        self.current_frame = 0
        self.current_action = 'idle_down'
        self.animation_delay = 80
        self.image = pygame.transform.scale(self.action_images_scaled[self.current_action][self.current_frame], (NPC_STATS[self.type]["SIZE"], NPC_STATS[self.type]["SIZE"]))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.last_update = 0
        self.last_attack = 0
        self.health = NPC_STATS[self.type]["MAX_HEALTH"]
        self.dead = False
        self.triggered = False
        self.attack_sound = Sounds()
        self.blast = Sounds()
        self.die_sound = Sounds()
        self.attack_sound.load_sound(sound_paths['attack_skeleton'])
        self.blast.load_sound(sound_paths['blast'])
        self.die_sound.load_sound(sound_paths[NPC_STATS[self.type]["DIE_SOUND"]])

    def draw(self, screen, map):
        now = pygame.time.get_ticks()
        if not self.dead:
            self.draw_health_bar(screen, self.rect.x - map.x_offset + NPC_STATS[self.type]["SIZE"] // 2 - NPC_STATS[self.type]["MAX_HEALTH"] // 2, self.rect.y - map.y_offset - 10, self.health, NPC_STATS[self.type]["MAX_HEALTH"])
            if now - self.last_update > self.animation_delay:
                self.update_frame()
        else:
            self.current_action = 'death'
            final_frame = 5 if self.type == 'SKELETON' else 8
            if now - self.last_update > self.animation_delay and self.current_frame != len(self.action_images_scaled[self.current_action]) - 1:
                self.update_frame()
            if self.current_frame == len(self.action_images_scaled[self.current_action]) - 1:
                self.image = pygame.transform.scale(self.action_images_scaled['death'][final_frame], (NPC_STATS[self.type]["SIZE"], NPC_STATS[self.type]["SIZE"]))
        screen.blit(self.image, (self.rect.x - map.x_offset, self.rect.y - map.y_offset))

    def update_frame(self):
        self.last_update = pygame.time.get_ticks()
        self.current_frame = (self.current_frame + 1) % len(self.action_images_scaled[self.current_action])
        self.image = pygame.transform.scale(self.action_images_scaled[self.current_action][self.current_frame], (NPC_STATS[self.type]["SIZE"], NPC_STATS[self.type]["SIZE"]))

    def draw_health_bar(self, screen, x, y, health, max_health):
        fill = (health / max_health) * NPC_STATS[self.type]["MAX_HEALTH"]
        outline_rect = pygame.Rect(x, y, NPC_STATS[self.type]["MAX_HEALTH"], 8)
        fill_rect = pygame.Rect(x, y, fill, 8)
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(screen, (0, 0, 0), outline_rect, 2)

    def set_direction(self, dx, dy):
        if dx == 0 and dy == 0:
            action = 'idle_left'
        elif dx > 0:
            if dy == 0:
                action = 'walk_right'
            elif dy > 0:
                action = 'walk_down'
            else:
                action = 'walk_up'
        else:
            if dy == 0:
                action = 'walk_left'
            elif dy > 0:
                action = 'walk_down'
            else:
                action = 'walk_up'
        if self.current_action != action:
            self.current_action = action
            self.current_frame = 0
            self.image = pygame.transform.scale(self.action_images_scaled[self.current_action][self.current_frame], (NPC_STATS[self.type]["SIZE"], NPC_STATS[self.type]["SIZE"]))

    def check_for_player(self, player, map):
        for projectile in player.projectiles:
            self_rect = pygame.Rect(self.rect.x - map.x_offset, self.rect.y - map.y_offset, NPC_STATS[self.type]["SIZE"], NPC_STATS[self.type]["SIZE"])
            if self_rect.colliderect(projectile) and not self.dead:
                self.health -= 1.5
                projectile.collided = True
                self.blast.play_sound()
                self.blast.played = True
                if self.health < 1:
                    self.dead = True
                    self.die_sound.play_sound()

        if not self.triggered:
            player_tile_x = player.rect.centerx // TEXTURE_SIZE
            player_tile_y = player.rect.centery // TEXTURE_SIZE
            npc_tile_x = self.rect.centerx // TEXTURE_SIZE
            npc_tile_y = self.rect.centery // TEXTURE_SIZE

            distance = math.sqrt((player_tile_x - npc_tile_x) ** 2 + (player_tile_y - npc_tile_y) ** 2)
            if distance <= 7:
                self.triggered = True

        if self.triggered and not self.dead:
            path = find_bfs_path(self, player, map)

            if path and len(path) > 1:
                next_tile = path[1]
                dx = (next_tile[0] * TEXTURE_SIZE) - self.rect.x
                dy = (next_tile[1] * TEXTURE_SIZE) - self.rect.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance > 0:
                    dx_normalized = dx / distance
                    dy_normalized = dy / distance
                    self.set_direction(dx_normalized, dy_normalized)
                    self.rect.x += dx_normalized * NPC_STATS[self.type]["SPEED"]
                    self.rect.y += dy_normalized * NPC_STATS[self.type]["SPEED"]
            else:
                self.current_action = f'attack_{self.current_action.split("_")[1]}'
                now = pygame.time.get_ticks()
                if now - self.last_attack > 500:
                    player.stats.current_health -= NPC_STATS[self.type]["DAMAGE"]
                    self.attack_sound.play_sound()
                    self.last_attack = now