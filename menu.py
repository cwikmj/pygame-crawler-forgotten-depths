import pygame as pygame
from settings import *

pygame.font.init()
vinque = pygame.font.Font("./vinque.otf", 36)
menu_image = pygame.image.load("assets/menu.png")
start_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
exit_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)

def display_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def loading_game(screen):
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (139, 69 ,19), start_rect, border_radius=10)
    display_text("loading ...", vinque, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2)
    pygame.display.update()

def welcome_screen(screen):
    screen.blit(menu_image, (0, 0))
    display_text("The Forgotten Depths", vinque, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2 - 100)
    pygame.draw.rect(screen, (139, 69 ,19), start_rect, border_radius=10)
    display_text("Start", vinque, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2)
    pygame.draw.rect(screen, (139, 69 ,19), exit_rect, border_radius=10)
    display_text("Exit", vinque, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 75)

def pause_screen(screen):
    game_state = screen.copy()
    overlay = pygame.Surface(screen.get_size())
    overlay.set_alpha(1)
    overlay.fill((100, 100, 100))
    screen.blit(game_state, (0, 0))
    screen.blit(overlay, (0, 0))

    pygame.draw.rect(screen, BACKGROUND, (WIDTH // 2 - 150, HEIGHT // 2 - 140, 300, 50), border_radius=10)
    display_text("game paused", vinque, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2 - 120)
    pygame.draw.rect(screen, BUTTON, (WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50), border_radius=10)
    display_text("(r)esume", vinque, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2)
    pygame.draw.rect(screen, BUTTON, (WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50), border_radius=10)
    display_text("(q)uit", vinque, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 75)

def complete_screen(screen, map, clock):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(0)
    for alpha in range(0, 255, 5):
        overlay.set_alpha(alpha)
        screen.fill(BACKGROUND)
        map.update_maze(screen)
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)

    screen.fill(BACKGROUND)
    display_text("CONGRATULATIONS! Level complete", vinque, BUTTON, screen, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    pygame.time.delay(2500)
    screen.fill(BACKGROUND)

def game_over_screen(screen):
    game_state = screen.copy()
    overlay = pygame.Surface(screen.get_size())
    overlay.set_alpha(1)
    overlay.fill((100, 100, 100))
    screen.blit(game_state, (0, 0))
    screen.blit(overlay, (0, 0))

    pygame.draw.rect(screen, BACKGROUND, (WIDTH // 2 - 150, HEIGHT // 2 - 140, 300, 50), border_radius=10)
    display_text("game over", vinque, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2 - 120)
    pygame.draw.rect(screen, BUTTON, (WIDTH // 2 - 100, HEIGHT // 2, 200, 50), border_radius=10)
    display_text("(q)uit", vinque, (0, 0, 0), screen, WIDTH // 2, HEIGHT // 2 + 25)