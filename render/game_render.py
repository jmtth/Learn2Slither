import pygame
import const as c
from render.popup_render import Popup


class GameRender:
    """Responsible for rendering the game state to the screen. """
    def __init__(self, config):
        self.config = config
        self.gameover_show = False

    def draw(self, screen, env):
        """Draws the current game state to the screen,
        including the grid, snake, fruits, and menu.

        If the game is over, it shows the game over screen.
        """
        if not env.game_over:
            screen.fill(c.BG_COLOR)
            self.draw_grid(screen)
            self.draw_snake(screen, env.snake)
            self.draw_fruits(screen, env.fruits)
            self.draw_menu(screen, env.score, env.snake.get_size())
        if env.game_over and not self.gameover_show:
            self.gameover_screen(screen)

    def draw_grid(self, screen):
        """Draws the grid lines on the game area
        based on the number of cells and cell size.
        """
        nb_cells = self.config.game.nb_cells
        cell_size = self.config.cell_size
        for x in range(0, (nb_cells + 1) * cell_size, cell_size):
            pygame.draw.line(
                screen,
                c.GRID_COLOR,
                (x, 0),
                (x, self.config.render.game_height),
                c.GRID_LINE_WIDTH
            )
        for y in range(0, (nb_cells + 1) * cell_size, cell_size):
            pygame.draw.line(
                screen,
                c.GRID_COLOR,
                (0, y),
                (self.config.render.screen_width, y),
                c.GRID_LINE_WIDTH
            )

    def draw_snake(self, screen, snake):
        """Draws the snake on the screen by
        iterating through its body segments.
        """
        cell_size = self.config.cell_size
        for segment in snake.body:
            pygame.draw.rect(
                screen,
                c.BLUE,
                (segment[0]*cell_size,
                 segment[1]*cell_size,
                 cell_size, cell_size)
            )

    def draw_fruits(self, screen, fruits):
        """Draws the fruits on the screen by
        iterating through the list of fruits.
        """
        cell_size = self.config.cell_size
        for fruit in fruits:
            pygame.draw.rect(
                screen,
                fruit.color,
                (fruit.position[0]*cell_size,
                 fruit.position[1]*cell_size,
                 cell_size, cell_size)
            )

    def draw_menu(self, screen, score, size):
        """Draws the menu area below the game area,
        displaying the current score and snake length.
        """
        GAME_WIDTH = self.config.render.screen_width
        GAME_HEIGHT = self.config.render.game_height
        pos_menu = (0, GAME_HEIGHT)
        menu_rect = pygame.Rect(0, pos_menu[1], GAME_WIDTH, c.MENU_HEIGHT)
        pygame.draw.rect(screen, c.MENU_COLOR, menu_rect)
        pygame.draw.rect(screen, c.MENU_TEXT_COLOR, menu_rect, 4)
        pygame.draw.line(screen, c.MENU_TEXT_COLOR,
                         (GAME_WIDTH // 2, pos_menu[1]),
                         (GAME_WIDTH // 2, pos_menu[1] + c.MENU_HEIGHT), 2)
        pygame.draw.line(screen, c.MENU_TEXT_COLOR,
                         (0, pos_menu[1] + c.MENU_FONT_SIZE),
                         (GAME_WIDTH,  pos_menu[1] + c.MENU_FONT_SIZE), 2)
        menu_font = pygame.font.SysFont(None, c.MENU_FONT_SIZE)
        value_font = pygame.font.SysFont(None, c.MENU_FONT_SIZE*2)
        marge = (10, 10)

        # Draw Score
        score_text = menu_font.render("Score:", True, c.MENU_TEXT_COLOR)
        score_text_height = score_text.get_height() + 10 + marge[1]
        x = (GAME_WIDTH // 2 - score_text.get_width()) // 2
        screen.blit(score_text, (x, pos_menu[1] + marge[1]))

        score_value_text = value_font.render(f"{score}", True, c.GREEN)
        x = (GAME_WIDTH // 2 - score_value_text.get_width()) // 2
        y = pos_menu[1] + marge[1] + score_text.get_height() + 10
        score_space = c.MENU_HEIGHT - score_text_height
        y = pos_menu[1] + score_text_height + score_space // 2
        y = y - score_value_text.get_height() // 2
        screen.blit(score_value_text, (x, y))

        # Draw Snake Length
        length_text = menu_font.render("Length:", True, c.MENU_TEXT_COLOR)
        x = GAME_WIDTH // 2 + (GAME_WIDTH // 2 - length_text.get_width()) // 2
        screen.blit(length_text, (x, pos_menu[1] + marge[1]))

        length_value_text = value_font.render(f"{size}", True, c.GREEN)
        x = GAME_WIDTH // 2
        x = x + (GAME_WIDTH // 2 - length_value_text.get_width()) // 2
        y = pos_menu[1] + marge[1] + length_text.get_height() + 10
        value_space = (length_text.get_height() + 10 + marge[1])
        length_space = c.MENU_HEIGHT - value_space
        y = pos_menu[1] + length_text.get_height() + 10 + marge[1]
        y = y + length_space // 2 - length_value_text.get_height() // 2
        screen.blit(length_value_text, (x, y))

    def gameover_screen(self, screen):
        """ Displays the game over screen with a message
        when the game is over.
        """
        self.gameover_show = True
        # GAME_WIDTH = self.config.render.screen_width
        # GAME_HEIGHT = self.config.render.game_height
        gameover_font = pygame.font.SysFont(None, c.MENU_FONT_SIZE)
        # gameover_text = gameover_font.render("Game Over!", True, c.RED)
        # x = (GAME_WIDTH - gameover_text.get_width()) // 2
        # y = (GAME_HEIGHT - gameover_text.get_height()) // 2
        # screen.blit(gameover_text, (x, y))
        # pygame.display.flip()
        popup = Popup("Game Over!\n\nThanks for playing.",
                      gameover_font,
                      self.config,
                      400, 150)
        popup.show()
        popup.draw(screen)
        print("Game Over! Thanks for playing.")
        self.gameover = True
