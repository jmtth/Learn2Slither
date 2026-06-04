import pygame
from scenes.scene import Scene
import const as c


class GameSettings(Scene):

    @property
    def nb_cells(self):
        return self.app.config.game.nb_cells

    @nb_cells.setter
    def nb_cells(self, value):
        self.app.config.game.nb_cells = value

    @property
    def speed(self):
        return self.app.config.render.fps

    @speed.setter
    def speed(self, value):
        self.app.config.render.fps = value

    @property
    def screen_width(self):
        return self.app.config.render.screen_width

    def __init__(self, app):
        self.app = app
        self.nb_cells_index = 0
        self.speed_index = 0
        self.font = pygame.font.Font(
            "assets/PressStart2P-Regular.ttf", 18)
        self.font_title = pygame.font.Font(
            "assets/PressStart2P-Regular.ttf", 26)
        self.font_instructions = pygame.font.Font(
            "assets/PressStart2P-Regular.ttf", 12)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.nb_cells_index = max(0, self.nb_cells_index - 1)
                self.nb_cells = c.CELLS_OPTIONS[self.nb_cells_index]
            if event.key == pygame.K_RIGHT:
                self.nb_cells_index = min(
                    len(c.CELLS_OPTIONS) - 1, self.nb_cells_index + 1)
                self.nb_cells = c.CELLS_OPTIONS[self.nb_cells_index]
            if event.key == pygame.K_UP:
                self.speed_index = min(
                    len(c.FPS_OPTIONS) - 1, self.speed_index + 1)
                self.speed = c.FPS_OPTIONS[self.speed_index]
            if event.key == pygame.K_DOWN:
                self.speed_index = max(0, self.speed_index - 1)
                self.speed = c.FPS_OPTIONS[self.speed_index]
            if event.key == pygame.K_ESCAPE:
                from scenes.mainmenu_scene import MainMenuScene
                self.app.change_scene(MainMenuScene(self.app))

    def update(self):
        pass

    def draw(self, screen):
        pygame.display.set_caption('Learn2Slither Snake: Game Settings')
        screen.fill(c.BLACK)
        speed = self.speed
        size = self.nb_cells
        title = self.font_title.render("LEARN 2 SLITHER", True, c.GREEN)
        screen.blit(title, title.get_rect(center=(self.screen_width // 2, 80)))
        board_size_text = self.font.render(
            f"BOARD SIZE: {size}/{c.CELLS_OPTIONS[-1]}", True, (255, 255, 255))
        speed_text = self.font.render(f"SPEED: {speed}", True, (255, 255, 255))
        screen.blit(board_size_text, board_size_text.get_rect(
            center=(self.screen_width // 2, 150)))
        screen.blit(speed_text, speed_text.get_rect(
            center=(self.screen_width // 2, 200)))
        instructions = "← → to change board size \n"
        instructions = instructions + "↑ ↓ to adjust speed | ESC to return"
        lines = instructions.split("\n")
        for i, line in enumerate(lines):
            txt = self.font_instructions.render(line, True, (180, 180, 180))
            screen.blit(txt, txt.get_rect(
                center=(self.screen_width // 2, 250 + i * 30)))
