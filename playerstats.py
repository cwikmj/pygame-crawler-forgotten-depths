import pygame
from menu import *
from sounds import *
from player import *

pygame.init()
vinque = pygame.font.Font("./vinque.otf", 16)

class PlayerStats:
    def __init__(self, player, health, mana, regeneration_rate):
        self.max_health = 100
        self.current_health = health
        self.max_mana = 100
        self.current_mana = mana
        self.health_potions = 0
        self.mana_potions = 0
        self.keys = 0
        self.health_potion_img = pygame.transform.scale(pygame.image.load(f'assets/spells/health.png').convert_alpha(), (TEXTURE_SIZE, TEXTURE_SIZE))
        self.mana_potion_img = pygame.transform.scale(pygame.image.load(f'assets/spells/mana.png').convert_alpha(), (TEXTURE_SIZE, TEXTURE_SIZE))
        self.key_img = pygame.transform.scale(pygame.image.load(f'assets/spells/key.png').convert_alpha(), (TEXTURE_SIZE, TEXTURE_SIZE))
        self.regeneration_rate = regeneration_rate
        self.last_regeneration_time = pygame.time.get_ticks()
        self.drink = Sounds()
        self.drink.load_sound(sound_paths['drink'])

    def update(self):
        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_h] and self.current_health < 99 and self.health_potions > 0:
            self.health_potions -= 1
            self.current_health = min(self.current_health + 40, 100)
            self.drink.play_sound()
        
        if keys[pygame.K_m] and self.current_mana < 99 and self.mana_potions > 0:
            self.mana_potions -= 1
            self.current_mana = min(self.current_mana + 40, 100)
            self.drink.play_sound()
        
        if now - self.last_regeneration_time >= 2000:
            self.current_mana = min(self.current_mana + self.regeneration_rate, self.max_mana)
            self.last_regeneration_time = now

    def draw_bar(self, screen, start_color, end_color, bar_rect, bar_width, bar_height):
        if bar_width > 0:
            pygame.draw.rect(screen, start_color, bar_rect)
            gradient = pygame.Surface((bar_width, bar_height))
            for i in range(bar_width):
                ratio = i / bar_width
                color = (
                    int(start_color[0] * ratio + end_color[0] * (1 - ratio)),
                    int(start_color[1] * ratio + end_color[1] * (1 - ratio)),
                    int(start_color[2] * ratio + end_color[2] * (1 - ratio))
                )
                pygame.draw.line(gradient, color, (i, 0), (i, bar_height))
            screen.blit(gradient, (bar_rect.x, bar_rect.y))

    def draw_stats(self, player, screen):
        self.update()
        if self.current_health <= 0:
            player.current_action = 'death'       

        # HEALTH & MANA
        pygame.draw.rect(screen, (40, 40, 40), (5, 510, 220, 80), border_radius=10)
        health_bar_width = int(self.current_health / self.max_health * 200)
        health_bar_rect = pygame.Rect(15, 525, health_bar_width, 20)
        mana_bar_width = int(self.current_mana / self.max_mana * 200)
        mana_bar_rect = pygame.Rect(15, 560, mana_bar_width, 20)
        self.draw_bar(screen, (255, 0, 0), (128, 0, 0), health_bar_rect, health_bar_width, 20)
        self.draw_bar(screen, (0, 0, 255), (0, 0, 128), mana_bar_rect, mana_bar_width, 20)

        labels = ["Health:", "Mana:"]
        values = [f"{self.current_health} / {self.max_health}", f"{self.current_mana} / {self.max_mana}"]
        for i, (label, value) in enumerate(zip(labels, values)):
            label_surface = vinque.render(label, True, (255, 255, 255))
            value_surface = vinque.render(value, True, (255, 255, 255))
            screen.blit(label_surface, (20, 510 + i * 35))
            screen.blit(value_surface, (120, 510 + i * 35))

        # POTIONS
        pygame.draw.rect(screen, (40, 40, 40), (230, 510, 150, 80), border_radius=10)
        hp_surface = vinque.render(str(self.health_potions), True, (255, 255, 255))
        mana_surface = vinque.render(str(self.mana_potions), True, (255, 255, 255))
        screen.blit(hp_surface, (285, 520 + i * 35))
        screen.blit(mana_surface, (355, 520 + i * 35))
        screen.blit(self.health_potion_img, (240, 495 + i * 35))
        screen.blit(self.mana_potion_img, (310, 495 + i * 35))

        if self.keys != 0:
            pygame.draw.rect(screen, (40, 40, 40), (385, 510, 80, 80), border_radius=10)
            keys_surface = vinque.render(str(self.keys), True, (255, 255, 255))
            screen.blit(keys_surface, (440, 555))
            screen.blit(self.key_img, (400, 530))
