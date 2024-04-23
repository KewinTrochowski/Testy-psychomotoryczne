import pygame
import sys
import time, random
import database_json
import textwrap

class Results_Menu:
    def __init__(self):
        pygame.init()

        # Ustawienia ekranu
        self.SCREEN_WIDTH = 700
        self.SCREEN_HEIGHT = 900
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Ekran Startowy")

        # Kolory
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.GREEN = (0, 255, 0)

        # Czcionka
        self.font = pygame.font.Font(None, 36)
        self.start = None
        self.wait = None
        self.your_time = None
        self.running = True
        self.playing = False

    # Funkcja rysująca tekst na ekranie
    def draw_text(self, text, color, x, y):
        text_obj = self.font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_obj, text_rect)

    # Funkcja rysująca przyciski
    def draw_button(self, x, y, width, height, color, text, text_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + width and y < mouse[1] < y + height:
            pygame.draw.rect(self.screen, self.GRAY, (x, y, width, height))
            if click[0] == 1 and action:  # Only execute action if mouse button is pressed down
                action()
        else:
            pygame.draw.rect(self.screen, color, (x, y, width, height))

        self.draw_text(text, text_color, x + width / 2, y + height / 2)


    def button3_action(self):
        pygame.quit()
        sys.exit()

    def button4_action(self):
        time.sleep(0.2)
        import menu
        menu.main()


    # Główna pętla gry
    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(self.BLACK)

            dt = database_json.read_results()
            t = ["Brak", "Brak", "Brak"]
            for game in dt:
                if game == "Kolko":
                    t[0] = dt[game]
                elif game == "Oko":
                    t[1] = dt[game]
                elif game == "Ucho":
                    t[2] = dt[game]
            self.draw_text("Wyniki:", self.WHITE, self.SCREEN_WIDTH / 2, 100)
            self.draw_text(f"Kółko: {t[0]}", self.WHITE, self.SCREEN_WIDTH / 2, 150)
            self.draw_text(f"Oko: {t[1]}", self.WHITE, self.SCREEN_WIDTH / 2, 200)
            self.draw_text(f"Ucho: {t[2]}", self.WHITE, self.SCREEN_WIDTH / 2, 250)

            self.draw_button(150, 580, 400, 100, self.WHITE, "Menu", self.BLACK, self.button4_action)
            self.draw_button(150, 700, 400, 100, self.WHITE, "Wyjście", self.BLACK, self.button3_action)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

