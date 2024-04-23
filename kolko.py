import pygame
import sys
import numpy as np
import time
import random
import database_json

SPEED = 2
RANDOM_ANGLE = (0.5, 1)
RANDOM_WAIT = (0.5, 1)
TIME_TO_DELETE = 2
TIME_TO_APPEAR = 1

# Klasa reprezentująca okrąg środkowy
class CircleMiddle:
    def __init__(self, screen, color, radius, center, line_width):
        self.screen = screen
        self.color = color
        self.radius = radius
        self.center = center
        self.line_width = line_width

    # Metoda do rysowania okręgu
    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.center, self.radius, self.line_width)


# Klasa reprezentująca okrąg gracza
class CirclePlayer:
    def __init__(self, screen, color, radius, center, line_width):
        self.screen = screen
        self.color = color
        self.radius = radius
        self.center = center
        self.line_width = line_width
        self.is_up = True
        self.middle_center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        self.speed = SPEED

    # Metoda do rysowania okręgu
    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.center, self.radius)

    def change_position(self):
        a = self.middle_center[0] - self.center[0]
        b = self.middle_center[1] - self.center[1]
        c = np.sqrt(a ** 2 + b ** 2)
        angle = np.arcsin(b / c)
        if self.middle_center[0] - self.center[0] > 0:
            angle = np.pi - angle

        if self.is_up:
            new_center = (self.center[0] - 2 * (self.radius + self.line_width) * np.cos(angle),
                          self.center[1] + 2 * (self.radius + self.line_width) * np.sin(angle))
            self.is_up = False
        else:
            new_center = (self.center[0] + 2 * (self.radius + self.line_width) * np.cos(angle),
                          self.center[1] - 2 * (self.radius + self.line_width) * np.sin(angle))
            self.is_up = True
        self.center = new_center

    def rotate(self):
        angle = 1 / 360 * np.pi * self.speed
        x = self.center[0] - self.middle_center[0]
        y = self.center[1] - self.middle_center[1]
        new_x = x * np.cos(angle) - y * np.sin(angle)
        new_y = x * np.sin(angle) + y * np.cos(angle)
        self.center = (new_x + self.middle_center[0], new_y + self.middle_center[1])
        return angle


class Obstacle:
    # Klasa reprezentująca prostokątną przeszkodę
    def __init__(self, screen, color, vertices, width, height, line_width=5):
        self.screen = screen
        self.color = color
        self.width = width
        self.height = height
        self.vertices = vertices.copy()
        self.middle_center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        self.line_width = line_width
        self.is_up = True
        self.time = time.time()


    # Metoda do rysowania przeszkody
    def draw(self):
        pygame.draw.polygon(self.screen, self.color, self.vertices, 2)

    def rotate(self, angle, random_angle):
        # rotate the player circle by 1 degree
        new_angle = angle
        new_angle = new_angle + random_angle
        for i in range(len(self.vertices)):
            x = self.vertices[i][0] - self.middle_center[0]
            y = self.vertices[i][1] - self.middle_center[1]
            new_x = x * np.cos(new_angle) - y * np.sin(new_angle)
            new_y = x * np.sin(new_angle) + y * np.cos(new_angle)
            self.vertices[i] = (new_x + self.middle_center[0], new_y + self.middle_center[1])

    def change_position(self):
        for v in self.vertices:
            a = self.middle_center[0] - v[0]
            b = self.middle_center[1] - v[1]
            c = np.sqrt(a ** 2 + b ** 2)
            angle = np.arcsin(b / c)
            if self.middle_center[0] - v[0] > 0:
                angle = np.pi - angle

            new_center = (v[0] - 2 * (self.width + self.line_width) * np.cos(angle), v[1] + (self.height + self.line_width) * np.sin(angle))
            self.vertices[self.vertices.index(v)] = new_center

        self.is_up = False




class CircleGame:
    def __init__(self):
        # Inicjalizacja Pygame
        pygame.init()


        # Ustawienia ekranu
        self.SCREEN_WIDTH = 700
        self.SCREEN_HEIGHT = 900
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Skaczący okrąg")
        # set the screen position


        # Wczytanie obrazu tła
        self.background = pygame.image.load("background.jpg")
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Kolory
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Ustawienia okręgu środkowego
        self.RADIUS = 200
        self.middle_center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
        self.line_width = 5

        # Stworzenie obiektu okręgu środkowego
        self.middle_circle = CircleMiddle(self.screen, self.WHITE, self.RADIUS, self.middle_center, self.line_width)

        # Ustawienia okręgu gracza
        self.player_radius = 20
        self.player_line_width = 2
        self.player_center = (self.middle_center[0], self.middle_center[1] - self.RADIUS - self.player_radius)
        self.player_angle = 0

        # Stworzenie obiektu okręgu gracza
        self.player_circle = CirclePlayer(self.screen, self.WHITE, self.player_radius, self.player_center,
                                          self.player_line_width)

        # Ustawienia przeszkody
        self.obstacle_height = 50
        self.obstacle_width = 20
        self.obstacle_center = self.player_center[0] - self.obstacle_width // 2, self.player_center[1] - self.line_width
        self.starting_vertices = [(self.obstacle_center[0] - self.obstacle_width // 2, self.obstacle_center[1] - self.obstacle_height // 2),
                         (self.obstacle_center[0] + self.obstacle_width // 2, self.obstacle_center[1] - self.obstacle_height // 2),
                         (self.obstacle_center[0] + self.obstacle_width // 2, self.obstacle_center[1] + self.obstacle_height // 2),
                         (self.obstacle_center[0] - self.obstacle_width // 2, self.obstacle_center[1] + self.obstacle_height // 2)]
        # Stworzenie obiektu przeszkody
        self.obstacles = []

        # Zmienne do śledzenia czasu
        self.start_time = time.time()
        self.current_time = 0
        self.obstacle_timer = 0
        self.delete_timer = 0
        self.font = pygame.font.SysFont(None, 36)
        self.waits = TIME_TO_APPEAR

        self.button_width = 100
        self.button_height = 50
        self.button_color = (50, 50, 50)
        self.button_text_color = self.WHITE
        self.button_text = "Reset"
        self.button_font = pygame.font.SysFont(None, 24)
        self.button_rect = pygame.Rect(
            self.SCREEN_WIDTH // 2 - self.button_width // 2,
            self.SCREEN_HEIGHT - self.button_height - 20,
            self.button_width,
            self.button_height
        )
        self.button_rect_menu =  pygame.Rect(
            self.SCREEN_WIDTH // 2 - self.button_width // 2,
            self.SCREEN_HEIGHT - self.button_height - 30 - self.button_height ,
            self.button_width,
            self.button_height
        )


    # Metoda do obsługi zdarzeń
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player_circle.change_position()
                if event.key == pygame.K_r:
                    return "reset"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.button_rect.collidepoint(event.pos):
                        return "reset"
                    if self.button_rect_menu.collidepoint(event.pos):
                        self.show_menu()


    # Metoda główna rozpoczynająca pętlę gry
    def run(self):
        running = True
        fps = 120
        clock = pygame.time.Clock()
        while running:
            clock.tick(fps)
            if self.handle_events() == "reset":
                running = False
            self.screen.blit(self.background, (0, 0))
            self.middle_circle.draw()
            self.player_circle.draw()
            self.player_angle += self.player_circle.rotate()
            if self.current_time - self.obstacle_timer > self.waits:
                obstacle = Obstacle(self.screen, self.WHITE, self.starting_vertices, self.obstacle_width,
                                    self.obstacle_height, self.line_width)
                random_angle = random.uniform(RANDOM_ANGLE[0], RANDOM_ANGLE[1]) * np.pi / 2
                obstacle.rotate(self.player_angle, random_angle)
                if random.random() > 0.5:
                    obstacle.change_position()
                self.obstacles.append(obstacle)
                self.obstacle_timer = self.current_time
                self.waits = random.uniform(RANDOM_WAIT[0], RANDOM_WAIT[1])

            if len(self.obstacles) > 0 and time.time() - self.obstacles[0].time > TIME_TO_DELETE:
                self.obstacles.pop(0)

            for obstacle in self.obstacles:
                obstacle.draw()

            if self.hit_obstacle():
                running = False
            self.update_timer()
            pygame.display.flip()
        database_json.save_results(round(self.current_time, 2), "Kolko")
        self.end_game()

    def update_timer(self):
        current_time = round((time.time() - self.start_time),2)
        self.draw_timer(current_time)
        self.current_time = current_time

    def draw_timer(self, current_time):
        timer_text = self.font.render("Czas: " + str(current_time), True, self.WHITE)
        self.screen.blit(timer_text, (10, 10))

    def show_menu(self):
        import menu
        menu.main()


    def hit_obstacle(self):
        for obstacle in self.obstacles:
            # Extract vertices of the obstacle rectangle
            x1, y1 = obstacle.vertices[0]
            x2, y2 = obstacle.vertices[1]
            x3, y3 = obstacle.vertices[2]
            x4, y4 = obstacle.vertices[3]

            # Check if circle center is inside the rectangle defined by its vertices
            if (self.player_circle.center[0] >= min(x1, x2, x3, x4) and
                    self.player_circle.center[0] <= max(x1, x2, x3, x4) and
                    self.player_circle.center[1] >= min(y1, y2, y3, y4) and
                    self.player_circle.center[1] <= max(y1, y2, y3, y4)):
                if obstacle.is_up == self.player_circle.is_up:
                    return True
        return False

    def end_game(self):
        running = True
        fps = 120
        clock = pygame.time.Clock()
        while running:
            clock.tick(fps)
            if self.handle_events() == "reset":
                running = False
            self.screen.fill(self.BLACK)

            end_text = self.font.render(f"Koniec gry", True, self.WHITE)
            text_width, text_height = self.font.size("Koniec gry")  # Get the width and height of the rendered text
            text_x = (self.SCREEN_WIDTH - text_width) // 2  # Calculate the x-coordinate for centering
            text_y = (self.SCREEN_HEIGHT - text_height) // 4  # Calculate the y-coordinate for centering
            self.screen.blit(end_text, (text_x, text_y))

            time_text = self.font.render(f"Czas: {round(self.current_time, 2)}", True, self.WHITE)
            time_text_width, time_text_height = self.font.size(
                f"Czas: {round(self.current_time, 2)}")  # Get the width and height of the time text
            time_text_x = (self.SCREEN_WIDTH - time_text_width) // 2  # Calculate the x-coordinate for centering
            time_text_y = text_y + text_height + 10  # Place time text below "Koniec gry"
            self.screen.blit(time_text, (time_text_x, time_text_y))


            pygame.draw.rect(self.screen, self.button_color, self.button_rect)
            button_text_surface = self.button_font.render(self.button_text, True, self.button_text_color)
            button_text_rect = button_text_surface.get_rect(center=self.button_rect.center)
            self.screen.blit(button_text_surface, button_text_rect)

            pygame.draw.rect(self.screen, self.button_color, self.button_rect_menu)
            button_text_surface = self.button_font.render("Menu", True, self.button_text_color)
            button_text_rect = button_text_surface.get_rect(center=self.button_rect_menu.center)
            self.screen.blit(button_text_surface, button_text_rect)

            pygame.display.flip()

        self.reset_game()

    def reset_game(self):
        # Reset game state to initial values
        self.start_time = time.time()
        self.current_time = 0
        self.obstacles.clear()
        self.player_circle.center = self.player_center
        self.player_circle.is_up = True
        self.player_angle = 0
        self.obstacle_timer = 0
        self.delete_timer = 0
        self.waits = 1
        self.run()


