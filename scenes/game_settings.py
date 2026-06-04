import pygame
from scenes.scene import Scene
from scenes.mainmenu_scene import MainMenuScene
import render.button_render as button
import const as c


class GameSettings(Scene):
    def __init__(self, app):
        self.app = app
        self.nb_cells_index = 0
        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 18)
        self.font_title = pygame.font.Font("assets/PressStart2P-Regular.ttf", 26)

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.app.config.nb_cells = c.NB_CELLS_SETTINGS[self.nb_cells_index - 1 if self.nb_cells_index - 1 >0 else 0]
                if event.key == pygame.K_RIGHT:
                    self.app.config.nb_cells = c.NB_CELLS_SETTINGS[self.nb_cells_index + 1 if self.nb_cells_index + 1 < len(c.NB_CELLS_SETTINGS) else len(c.NB_CELLS_SETTINGS) - 1]
                if event.key == pygame.K_ESCAPE:
                    self.app.change_scene(MainMenuScene(self.app))

    def update(self):
        pass

    def draw(self, screen):
        title = self.font_title.render("LEARN 2 SLITHER", True, c.GREEN)
        screen.blit(title, title.get_rect(center=(c.SCREEN_SIZE[0] // 2, 80)))
        self.start_button.draw(screen)
        self.settings_button.draw(screen)
        self.quit_button.draw(screen)
        vol_display = "MUTED" if muted else f"VOLUME: {volume}/10"
        volume_text = self.font.render(vol_display, True, (255, 255, 255))
        screen.blit(volume_text, volume_text.get_rect(center=(c.SCREEN_SIZE[0] // 2, 150)))

        instructions = self.font.render("← → to adjust | M to mute | ESC to return", True, (180, 180, 180))
        screen.blit(instructions, instructions.get_rect(center=(c.SCREEN_SIZE[0] // 2, 250)))
