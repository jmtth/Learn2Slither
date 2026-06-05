import pygame


class Button:
    """Represents a clickable button in the UI. """
    def __init__(self,
                 x, y, w, h,
                 text,
                 callback,
                 font, base_color, hover_color, click_color=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.click_color = click_color if click_color else hover_color
        self.hovered = False
        self.clicked = False
        self.click_timer = 0

    def draw(self, screen):
        """Draws the button on the given screen,
        changing color based on hover and click states.
        """
        if self.clicked and pygame.time.get_ticks() - self.click_timer < 100:
            color = self.click_color
        else:
            color = self.hover_color if self.hovered else self.base_color

        pygame.draw.rect(screen, color, self.rect, border_radius=8)

        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        """Handles mouse events to update hover and click states,
        and triggers the callback when clicked."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            self.clicked = True
            self.click_timer = pygame.time.get_ticks()
            self.callback()
