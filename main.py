import pygame
import sys
from settings import *
from menu import *
from sounds import *
from map import *
from player import *
from npc import *

# PRE-GAME INIT
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((RES))
loading_game(screen)

# INIT
map = Map(X_OFFSET, Y_OFFSET)
player = Player(PLAYER_X, PLAYER_Y, PLAYER_ANGLE)
menu_sound = Sounds()
menu_sound.load_sound(sound_paths["menu_click"])
npc_group = pygame.sprite.Group()
skeleton_positions = [(200, 500), (150, 120), (750, 450), (900, 550), (1100, 1000), (900, 150), (1800, 150), (1870, 180)]
skeletons = [NPC(x, y, 'SKELETON') for x, y in skeleton_positions]
skelet_demon = NPC(1600, 1100, 'SKELETON_DEMON')
npc_group.add(*skeletons, skelet_demon)
chest_group = pygame.sprite.Group()
chest_positions = [((3, 3), (2, 3), 'health'), ((22, 4), (23, 2), 'mana'), ((27, 28), (29, 27), 'health', 2), ((46, 3), (47, 1), 'key')]
chests = [Chest(*position) for position in chest_positions]
chest_group.add(*chests)

# GAME STATE
welcome = True
paused = False
game_over = False
level_complete = False

# GAME LOOP
while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if welcome:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                welcome = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if start_rect.collidepoint(mouse_x, mouse_y):
                    welcome = False
                    menu_sound.play_sound()
                elif exit_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not game_over:
                    paused = True
                    menu_sound.play_sound()
                elif event.key == pygame.K_r:
                    menu_sound.play_sound()
                    paused = False
                elif paused or game_over and event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

    if welcome:
        welcome_screen(screen)
    elif paused:
        pause_screen(screen)
    elif player.dead:
        game_over_screen(screen)
        game_over = True
    elif map.complete and not any(not npc.dead for npc in npc_group):
        complete_screen(screen, map, clock)
        map.complete = False
        player.dead = True
    else:
        # GAME LOGIC
        screen.fill(BACKGROUND)
        map.update_maze(screen)
        player.movement(map)
        for npc in npc_group:
            npc.check_for_player(player, map)
            npc.draw(screen, map)
        player.draw(screen, map)
        for chest in chest_group:
            chest.check_proximity(player, map)

    pygame.display.update()
    pygame.display.set_caption(f'The Forgotten Depths - {clock.get_fps() :.1f}')
