import pygame


class Button:
    def __init__(self, x, y, w, h, text, callback, font, base_color, hover_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.hovered = False

    def draw(self, screen):
        color = self.hover_color if self.hovered else self.base_color
        pygame.draw.rect(screen, color, self.rect)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            self.callback()