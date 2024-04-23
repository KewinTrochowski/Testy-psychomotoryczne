import pygame
import sys
from kolko import CircleGame
from refleks_oko import ReflexEye
from refleks_ucho import ReflexEar
from wyniki import Results_Menu
import time
import os

# Ustawienie pozycji okna
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (800, 100)
# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ekran Startowy")

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Funkcja rysująca tekst na ekranie
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Funkcja rysująca przyciski
def draw_button(x, y, width, height, color, text, font, text_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, GRAY, (x, y, width, height))
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    draw_text(text, font, text_color, screen, x + width / 2, y + height / 2)

# Funkcje akcji dla przycisków
def button1_action():
    time.sleep(0.2)
    game = CircleGame()  # Tworzenie obiektu gry
    game.run()

def button2_action():
    time.sleep(0.2)
    game = ReflexEye()  # Tworzenie obiektu gry
    game.run()

def button3_action():
    time.sleep(0.2)
    game = ReflexEar()  # Tworzenie obiektu gry
    game.run()

def button4_action():
    time.sleep(0.2)
    game = Results_Menu()  # Tworzenie obiektu gry
    game.run()

def button5_action():
    pygame.quit()
    sys.exit()

# Główna funkcja startowa
def main():
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        w = 300
        h = 100
        x = SCREEN_WIDTH // 2 - w // 2
        y = SCREEN_HEIGHT // 2 - 4*h
        draw_button(x, y, w, h, WHITE, "Skaczące kółko", font, BLACK, button1_action)
        draw_button(x, y + 1.5*h, w, h, WHITE, "Refleks oko", font, BLACK, button2_action)
        draw_button(x, y + 3*h, w, h, WHITE, "Refleks ucho", font, BLACK, button3_action)
        draw_button(x, y + 4.5*h, w, h, WHITE, "Wyniki", font, BLACK, button4_action)
        draw_button(x, y + 6 * h, w, h, WHITE, "Wyjście", font, BLACK, button5_action)
        pygame.display.update()



if __name__ == "__main__":
    main()
