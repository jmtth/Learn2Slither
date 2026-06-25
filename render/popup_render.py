import helpers.const as c
import pygame
from helpers.config import AppConfig


class Popup:
    def __init__(self,
                 message: str,
                 font,
                 config: AppConfig,
                 width=400,
                 height=150):
        self.config = config
        self.message = message
        self.font = font
        self.width = width
        self.height = height
        self.rect = pygame.Rect(
            (config.render.screen_width - width) // 2,
            (config.render.game_height - height) // 2,
            width, height)
        self.active = False

    def show(self, message: str = ""):
        self.active = True
        if message != "":
            self.message = message

    def hide(self):
        self.active = False

    def draw(self, screen):
        if not self.active:
            return

        pygame.draw.rect(screen, (20, 20, 20), self.rect, border_radius=10)
        pygame.draw.rect(screen, (c.RED), self.rect, 2, border_radius=10)

        lines = self.message.split("\n")
        for i, line in enumerate(lines):
            txt = self.font.render(line, True, c.RED)
            screen.blit(txt, txt.get_rect(center=(
                self.config.render.screen_width // 2,
                self.rect.y + 40 + i * 30))
                )
