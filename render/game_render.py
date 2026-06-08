import pygame
import const as c
from render.popup_render import Popup


class GameRender:
    """Responsible for rendering the game state to the screen. """
    def __init__(self, config):
        self.config = config
        self.gameover_shown = False
        self.pause_shown = False

    def draw(self, screen, env):
        """Draws the current game state to the screen,
        including the grid, snake, fruits, and menu.

        If the game is over, it shows the game over screen.
        """
        if not env.game_over and not env.paused:
            self.pause_shown = False
            screen.fill(c.BG_COLOR)
            self.draw_grid(screen)
            self.draw_snake(screen, env.snake)
            self.draw_fruits(screen, env.fruits)
            self.draw_menu(screen, env)
        if env.game_over and not self.gameover_shown:
            self.gameover_screen(screen)
            self.draw_menu(screen, env)
            return
        if env.paused and not self.pause_shown:
            self.draw_pause(screen)

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

    def draw_menu(self, screen, env):
        """Draws the menu area below the game area,
        displaying the current score and snake length.
        """
        GAME_WIDTH = self.config.render.screen_width
        GAME_HEIGHT = self.config.render.game_height
        margin = 3
        pos_menu = (0, GAME_HEIGHT)
        col_width = GAME_WIDTH // 4
        pos_x_col2 = col_width
        pos_x_col3 = 2 * col_width
        pos_x_col4 = 3 * col_width
        pos_y_row2 = pos_menu[1] + c.MENU_FONT_SIZE
        row_height = c.MENU_FONT_SIZE
        moves, size = env.move_count, env.snake.get_size()
        green_count = env.green_apples_eaten
        red_count = env.red_apples_eaten
        menu_rect = pygame.Rect(0, pos_menu[1], GAME_WIDTH, c.MENU_HEIGHT)
        pygame.draw.rect(screen, c.MENU_COLOR, menu_rect)
        pygame.draw.rect(screen, c.MENU_TEXT_COLOR, menu_rect, 4)
        # Vertical line separating the left and right sections of the menu
        pygame.draw.line(screen, c.MENU_TEXT_COLOR,
                         (GAME_WIDTH // 2, pos_menu[1]),
                         (GAME_WIDTH // 2, pos_menu[1] + c.MENU_HEIGHT), 2)
        # Horizontal line separating the header sections of the menu
        pygame.draw.line(screen, c.MENU_TEXT_COLOR,
                         (0, pos_menu[1] + c.MENU_FONT_SIZE),
                         (GAME_WIDTH,  pos_menu[1] + c.MENU_FONT_SIZE), 2)
        # Vertical lines separating moves and length sections
        pygame.draw.line(screen, c.MENU_TEXT_COLOR,
                         (col_width, pos_menu[1]),
                         (col_width, pos_menu[1] + c.MENU_HEIGHT), 2)
        # Vertical line separating green and red apples sections
        pygame.draw.line(screen, c.MENU_TEXT_COLOR,
                         (3 * col_width, pos_menu[1] + c.MENU_FONT_SIZE),
                         (3 * col_width, pos_menu[1] + c.MENU_HEIGHT), 2)
        # Horizontal line separating the apple header from the apple counts
        pygame.draw.line(screen, c.MENU_TEXT_COLOR,
                         (2 * col_width, pos_menu[1] + c.MENU_FONT_SIZE * 2),
                         (GAME_WIDTH,  pos_menu[1] + c.MENU_FONT_SIZE * 2), 2)
        header_font = pygame.font.Font(
            "assets/PressStart2P-Regular.ttf", c.MENU_FONT_HEADER_SIZE)
        value_font = pygame.font.Font(
            "assets/PressStart2P-Regular.ttf", c.MENU_FONT_VALUE_SIZE)
        counter_font = pygame.font.Font(
            "assets/PressStart2P-Regular.ttf", c.MENU_FONT_COUNTER_SIZE)

        # Draw moves Count
        moves_text = header_font.render("MOVES", True, c.MENU_TEXT_COLOR)
        x = (col_width - moves_text.get_width()) // 2
        y = pos_menu[1] + (row_height - moves_text.get_height()) // 2
        screen.blit(moves_text, (x, y + margin))

        if moves > 999:
            coeff = 1000
            moves_display = f"{moves / coeff:.1f}K"
        else:
            moves_display = str(moves)
        moves_value_text = value_font.render(f"{moves_display}", True, c.WHITE)
        x = (col_width - moves_value_text.get_width()) // 2
        remaining_space = c.MENU_HEIGHT - row_height
        y = pos_menu[1] + row_height + (
            remaining_space - moves_value_text.get_height()) // 2
        screen.blit(moves_value_text, (x, y))

        # Draw Snake Length
        length_text = header_font.render("LENGTH", True, c.MENU_TEXT_COLOR)
        x = GAME_WIDTH // 4 + (GAME_WIDTH // 4 - length_text.get_width()) // 2
        x = pos_x_col2 + (col_width - length_text.get_width()) // 2
        y = pos_menu[1] + (row_height - length_text.get_height()) // 2
        screen.blit(length_text, (x, y + margin))

        length_value_text = value_font.render(f"{size}", True, c.WHITE)
        x = pos_x_col2 + (col_width - length_value_text.get_width()) // 2
        remaining_space = c.MENU_HEIGHT - row_height
        y = pos_menu[1] + row_height + (
            remaining_space - length_value_text.get_height()) // 2
        screen.blit(length_value_text, (x, y))

        # Draw Snake Length
        apples_text = header_font.render("APPLES", True, c.MENU_TEXT_COLOR)
        x = pos_x_col3 + (col_width * 2 - apples_text.get_width()) // 2
        y = pos_menu[1] + (row_height - apples_text.get_height()) // 2
        screen.blit(apples_text, (x, y + margin))
        green_apples_text = header_font.render(
            "GREEN", True, c.MENU_TEXT_COLOR)
        x = pos_x_col3 + (col_width - green_apples_text.get_width()) // 2
        y = pos_y_row2 + (row_height - green_apples_text.get_height()) // 2
        screen.blit(green_apples_text, (x, y + margin))
        red_apples_text = header_font.render("RED", True, c.MENU_TEXT_COLOR)
        x = pos_x_col4 + (col_width - red_apples_text.get_width()) // 2
        screen.blit(red_apples_text, (x, y + margin))

        green_apples_value_text = counter_font.render(
            f"{green_count}", True, c.GREEN)
        x = pos_x_col3 + (col_width - green_apples_value_text.get_width()) // 2
        remaining_space = c.MENU_HEIGHT - (row_height * 2)
        y = pos_y_row2 + row_height + (
            remaining_space - green_apples_value_text.get_height()) // 2
        screen.blit(green_apples_value_text, (x, y))

        red_apples_value_text = counter_font.render(
            f"{red_count}", True, c.RED)
        x = pos_x_col4 + (col_width - red_apples_value_text.get_width()) // 2
        remaining_space = c.MENU_HEIGHT - (row_height * 2)
        y = pos_y_row2 + row_height + (
            remaining_space - red_apples_value_text.get_height()) // 2
        screen.blit(red_apples_value_text, (x, y))

    def gameover_screen(self, screen):
        """ Displays the game over screen with a message
        when the game is over.
        """
        self.gameover_shown = True
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

    def draw_pause(self, screen):
        """ Displays the pause screen with a message
        when the game is paused.
        """
        self.pause_shown = True
        pause_font = pygame.font.SysFont(None, c.MENU_FONT_SIZE)
        popup = Popup("Game Paused\n\nPress P to resume",
                      pause_font,
                      self.config,
                      400, 150)
        popup.show()
        popup.draw(screen)
        print("Game Paused. Press P to resume.")
        self.pause = True
