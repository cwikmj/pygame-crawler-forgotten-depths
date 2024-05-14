from settings import *
from sounds import *
from map import *
from projectiles import *
from playerstats import *
import pygame as pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.action_images = {}
        directions = ['up', 'down', 'left', 'right']
        for direction in directions:
            self.action_images[f'walk_{direction}'] = [pygame.image.load(f'assets/sprites/mage/walk/walk_{direction} ({i}).png').convert_alpha() for i in range(1, 9)]
            self.action_images[f'spell_{direction}'] = [pygame.image.load(f'assets/sprites/mage/spell/spell_{direction} ({i}).png').convert_alpha() for i in range(1, 7)]
            self.action_images[f'idle_{direction}'] = [pygame.image.load(f'assets/sprites/mage/idle/idle_{direction}.png').convert_alpha()]
        self.action_images['death'] = [pygame.image.load(f'assets/sprites/mage/death/death ({i}).png').convert_alpha() for i in range(1, 7)]
        
        self.action_images_scaled = {
            action: [pygame.transform.scale(image, (PLAYER_SIZE, PLAYER_SIZE)) for image in images]
            for action, images in self.action_images.items()
        }
        
        self.current_action = 'idle_right'
        self.current_frame = 0
        self.animation_delay = 50
        self.last_update = 0
        self.image = self.action_images_scaled[self.current_action][self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.angle = angle
        self.last_spell_time = 0
        self.arrow_blink_time = 0
        self.spell_shot = False
        self.projectiles = []
        self.dead = False
        self.stats = PlayerStats(self, PLAYER_MAX_HEALTH, PLAYER_MAX_MANA, 1)
        self.ambient = Sounds()
        self.game_over_sound = Sounds()
        self.fire = Sounds()
        self.blast = Sounds()
        self.ambient.load_sound(sound_paths['ambient'])
        self.game_over_sound.load_sound(sound_paths['game_over'])
        self.fire.load_sound(sound_paths['fire'])
        self.blast.load_sound(sound_paths['blast'])
        self.ambient.play_looped_sound()

    def set_action(self, action):
        if action in self.action_images_scaled:
            self.current_action = action
            self.arrow_blink_time = 0
            self.current_frame = 0
            self.image = self.action_images_scaled[self.current_action][self.current_frame]

    def draw(self, screen, map):
        self.stats.draw_stats(self, screen)
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_delay:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.action_images_scaled[self.current_action])
            self.image = self.action_images_scaled[self.current_action][self.current_frame]
            
            if self.current_action.startswith('spell'):
                if self.current_frame == len(self.action_images_scaled[self.current_action]) - 3:
                    projectile = Projectile(self.rect.x + PLAYER_SIZE // 2 - map.x_offset, self.rect.y + PLAYER_SIZE // 1.6 - map.y_offset, self.angle)
                    self.projectiles.append(projectile)
                    self.last_spell_time = now
                    self.stats.current_mana -= 2
                if self.current_frame == len(self.action_images_scaled[self.current_action]) - 1:
                    self.set_action('idle_' + self.current_action.split('_')[1])
                    self.spell_shot = False
            
        screen.blit(self.image, (self.rect.x - map.x_offset, self.rect.y - map.y_offset))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.stats.current_mana > 1 and not self.spell_shot and not self.current_action.startswith('death') and now - self.last_spell_time > 500:
            self.set_action('spell_' + self.current_action.split('_')[1])
            self.spell_shot = True
            self.fire.play_sound()
        elif not keys[pygame.K_SPACE]:
            self.spell_shot = False
            self.last_spell_time = 0

        for projectile in self.projectiles:
            projectile.update()
            projectile.draw(screen)
            if projectile.check_wall_collision(map):
                projectile.collided = True
            if projectile.exploded:
                self.blast.play_sound()
                self.projectiles.remove(projectile)

        if self.current_action == 'death' and self.current_frame == 5:
            self.dead = True
            self.ambient.stop_sound()
            self.game_over_sound.play_sound()
  
    def movement(self, map):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if not self.spell_shot:
            dx = (keys[pygame.K_d] - keys[pygame.K_a]) * PLAYER_SPEED
            dy = (keys[pygame.K_s] - keys[pygame.K_w]) * PLAYER_SPEED

        # WALL COLLISION + OFFSET
        if not self.is_wall_collision(dx, 0, map):
            if 0 <= self.rect.x + dx <= 2 * WIDTH - PLAYER_SIZE:
                self.rect.x += dx
                if self.rect.x < map.x_offset + SCROLL_TRESH:
                    map.x_offset = max(self.rect.x - SCROLL_TRESH, 0)
                elif self.rect.x > map.x_offset + WIDTH - PLAYER_SIZE - SCROLL_TRESH:
                    map.x_offset = min(self.rect.x + PLAYER_SIZE - WIDTH + SCROLL_TRESH, 2 * WIDTH)
        if not self.is_wall_collision(0, dy, map):
            if 0 <= self.rect.y + dy <= 2 * HEIGHT - PLAYER_SIZE:
                self.rect.y += dy
                if self.rect.y < map.y_offset + SCROLL_TRESH:
                    map.y_offset = max(self.rect.y - SCROLL_TRESH, 0)
                elif self.rect.y > map.y_offset + HEIGHT - PLAYER_SIZE - SCROLL_TRESH:
                    map.y_offset = min(self.rect.y + PLAYER_SIZE - HEIGHT + SCROLL_TRESH, 2 * HEIGHT)

        if dx == dy == 0:
            idle_actions_mapping = {'walk_up': 'idle_up', 'walk_down': 'idle_down', 'walk_left': 'idle_left', 'walk_right': 'idle_right'}
            if self.current_action in idle_actions_mapping:
                self.set_action(idle_actions_mapping[self.current_action])

        key_mapping = {pygame.K_w: (-math.pi / 2), pygame.K_d: (0), pygame.K_a: (math.pi), pygame.K_s: (math.pi / 2)}
        keys_pressed = [key for key in key_mapping.keys() if keys[key]]
        
        if keys_pressed:
            angles_sum_x = sum([math.cos(key_mapping[key]) for key in keys_pressed])
            angles_sum_y = sum([math.sin(key_mapping[key]) for key in keys_pressed])
            new_angle = math.atan2(angles_sum_y, angles_sum_x)
            
            if new_angle != self.angle:
                self.angle = new_angle
                
                if new_angle == -math.pi / 2:
                    self.set_action('walk_up')
                elif new_angle == 0:
                    self.set_action('walk_right')
                elif new_angle == math.pi:
                    self.set_action('walk_left')
                elif new_angle == math.pi / 2:
                    self.set_action('walk_down')

    def is_wall_collision(self, x, y, map):
        player_rect = self.rect.move(x, y)
        for row in map.maze:
            for tile in row:
                if tile[3]:
                    tile_rect = pygame.Rect(tile[1] * TEXTURE_SIZE, tile[0] * TEXTURE_SIZE, TEXTURE_SIZE, TEXTURE_SIZE)
                    if player_rect.colliderect(tile_rect):
                        return True
        return False