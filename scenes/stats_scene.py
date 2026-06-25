import pygame
from scenes.scene import Scene
import helpers.const as c
from stats.manage_csv import MyStats


class StatsScene(Scene):
    """Scene for displaying game statistics and performance metrics."""

    @property
    def screen_width(self):
        return self.app.config.render.screen_width

    @property
    def screen_height(self):
        return self.app.config.render.screen_height

    def __init__(self, app):
        self.app = app
        self.font = pygame.font.Font(
            "assets/PressStart2P-Regular.ttf", 16)
        self.font_title = pygame.font.Font(
            "assets/PressStart2P-Regular.ttf", 26)
        self.font_subtitle = pygame.font.Font(
            "assets/PressStart2P-Regular.ttf", 12)
        self.font_scores = pygame.font.Font(
            "assets/PressStart2P-Regular.ttf", 12)
        self.stats = MyStats()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from scenes.mainmenu_scene import MainMenuScene
                self.app.change_scene(MainMenuScene(self.app))

    def update(self):
        pass

    def draw(self, screen):
        pygame.display.set_caption('Learn2Slither Snake: Stats')
        screen.fill(c.BLACK)

        title = self.font_title.render("GAME STATS", True, c.GREEN)
        screen.blit(title, title.get_rect(center=(self.screen_width // 2, 50)))

        nb_player = 0 if self.stats.df.empty else self.stats.get_player_count()
        nb_game = 0 if self.stats.df.empty else self.stats.get_game_count()
        stats_info = f"Total Players: {nb_player} | Total Games: {nb_game}"
        stats_surf = self.font_subtitle.render(stats_info, True, c.CYAN)
        stats_rect = stats_surf.get_rect(center=(self.screen_width // 2, 120))
        screen.blit(stats_surf, stats_rect)

        rect = pygame.Rect(
            25, 150, self.screen_width - 50, self.screen_height - 200)
        pygame.draw.rect(screen, c.DARK_GRAY, rect, border_radius=8)
        text_surf = self.font.render(
            "Player  | Moves | Length | Apples", True, c.WHITE)
        text_rect = text_surf.get_rect(top=rect.top + 10, left=rect.left + 10)
        screen.blit(text_surf, text_rect)
        list_stats = [] if self.stats.df.empty else self.stats.get_top_scores()
        for i, stat in enumerate(list_stats):
            stat_text = f"{stat[0][:11]:<11}| {stat[1]:^8} | "
            stat_text += f"{stat[2]:^9} | {stat[3]:^8}"
            if i == 0:
                color = c.YELLOW
            else:
                color = c.LIGHT_GRAY
            stat_surf = self.font_scores.render(
                stat_text, True, color)
            stat_rect = stat_surf.get_rect(
                top=text_rect.bottom + 20 + i * 30, left=rect.left + 10)
            screen.blit(stat_surf, stat_rect)
        instructions = "[ESC] to return to main menu"
        txt = self.font_scores.render(instructions, True, (180, 180, 180))
        screen.blit(txt, txt.get_rect(
            center=(self.screen_width // 2, self.screen_height - 30)))
