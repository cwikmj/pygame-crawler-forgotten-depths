import pygame

sound_paths = {
    'ambient': 'assets/sounds/ambient.ogg',
    'attack_skeleton': 'assets/sounds/attack_skeleton.ogg',
    'blast': 'assets/sounds/blast.ogg',
    'die_boss': 'assets/sounds/die_boss.ogg',
    'die_skeleton': 'assets/sounds/die_skeleton.ogg',
    'drink': 'assets/sounds/drink.ogg',
    'final_door_open': 'assets/sounds/final_door_open.ogg',
    'fire': 'assets/sounds/fire.ogg',
    'game_over': 'assets/sounds/game_over.ogg',
    'key_found': 'assets/sounds/key_found.ogg',
    'menu_click': 'assets/sounds/menu_click.ogg'
}

class Sounds:
    def __init__(self):
        pygame.mixer.init(buffer=512)
        self.sound = None
        self.played = False

    def load_sound(self, sound_path):
        self.sound = pygame.mixer.Sound(sound_path)

    def play_sound(self):
        if self.sound is not None and not self.played:
            self.sound.play()
        else:
            self.played = False

    def play_looped_sound(self):
            if self.sound is not None:
                self.sound.play(-1)

    def stop_sound(self):
        if self.sound is not None:
            self.sound.stop()

# https://www.freeconvert.com/wav-to-ogg/download