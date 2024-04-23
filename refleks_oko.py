import pygame
import sys
import time, random
import database_json

class ReflexEye:
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

    # Funkcja akcji dla przycisków
    def button1_action(self):
        time.sleep(0.1)
        if not self.playing:
            self.game()

    def button2_action(self):
        if time.time() - self.start >=self.wait:
            self.your_time = time.time() - self.start - self.wait
            self.running = False
        else:
            self.your_time = "Za wcześnie!"
            self.running = False
        try:
            self.your_time = round(self.your_time, 2)
            database_json.save_results(self.your_time, "Oko")
        except:
            pass

    def button3_action(self):
        pygame.quit()
        sys.exit()

    def button4_action(self):
        time.sleep(0.2)
        import menu
        menu.main()

    def game(self):
        self.playing = True
        self.start = time.time()
        self.wait = random.randint(2, 5)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if time.time() - self.start < self.wait:
                self.screen.fill(self.WHITE)
            else:
                self.screen.fill(self.GREEN)

            self.draw_text("Gra polega na jak najszybszym wciśnięciu", self.BLACK, self.SCREEN_WIDTH / 2, 100)
            self.draw_text("przycisku po zmianie koloru tła na zielony.", self.BLACK, self.SCREEN_WIDTH / 2, 150)
            self.draw_button(150, 200, 400, 100, self.BLACK, "Wciśnij", self.WHITE, self.button2_action)

            pygame.display.flip()
        self.running = True
        time.sleep(0.1)
        self.playing = False



    # Główna pętla gry
    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(self.WHITE)

            self.draw_text("Gra polega na jak najszybszym wciśnięciu", self.BLACK, self.SCREEN_WIDTH / 2, 100)
            self.draw_text("przycisku po zmianie koloru tła na zielony.", self.BLACK, self.SCREEN_WIDTH / 2, 150)
            self.draw_button(150, 200, 400, 100, self.GREEN, "Start", self.BLACK, self.button1_action)
            if self.your_time is not None:
                if isinstance(self.your_time, str):
                    self.draw_text(self.your_time, self.BLACK, self.SCREEN_WIDTH / 2, 350)
                else:
                    self.draw_text("Twój czas to: " + str(round(self.your_time, 2)) + " sekund", self.BLACK, self.SCREEN_WIDTH / 2, 350)

            self.draw_button(150, 580, 400, 100, self.BLACK, "Menu", self.WHITE, self.button4_action)
            self.draw_button(150, 700, 400, 100, self.BLACK, "Wyjście", self.WHITE, self.button3_action)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = ReflexEye()
    game.run()
