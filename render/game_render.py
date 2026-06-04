class GameRender:
    # def __init__(self, game):
    #     self.game = game

    def draw(self, screen):
        screen.fill(c.BG_COLOR)  # Clear screen with background color
        self.draw_grid()  # Draw the grid
        
        self.snake.draw(self.screen)  # Draw the snake
        for fruit in self.fruits:
            fruit.draw(self.screen)  # Draw each fruit
        if self.gameover:
            self.gameover_screen()  # Show game over screen
        self.draw_menu()  # Draw the menu
        # Draw game elements here
        pygame.display.flip()  # Update the display

    def draw_grid(self):
        for x in range(0, c.NB_CELLS * c.CELL_SIZE, c.CELL_SIZE):
            pygame.draw.line(self.screen, c.GRID_COLOR, (x, 0), (x, c.GAME_HEIGHT), c.GRID_LINE_WIDTH)
        for y in range(0, c.NB_CELLS * c.CELL_SIZE, c.CELL_SIZE):
            pygame.draw.line(self.screen, c.GRID_COLOR, (0, y), (c.GAME_WIDTH, y), c.GRID_LINE_WIDTH)

    def draw_menu(self, score=0, snake_length=1):
        pos_menu = (0, c.GAME_HEIGHT)
        menu_rect = pygame.Rect(0, pos_menu[1], c.GAME_WIDTH, c.MENU_HEIGHT)
        pygame.draw.rect(self.screen, c.MENU_COLOR, menu_rect)
        pygame.draw.rect(self.screen, c.MENU_TEXT_COLOR, menu_rect, 4)  # Draw border
        pygame.draw.line(self.screen, c.MENU_TEXT_COLOR, (c.GAME_WIDTH // 2, pos_menu[1]), (c.GAME_WIDTH // 2, pos_menu[1] + c.MENU_HEIGHT), 2)  # Draw separator line
        pygame.draw.line(self.screen, c.MENU_TEXT_COLOR, (0, pos_menu[1] + c.MENU_FONT_SIZE), (c.GAME_WIDTH,  pos_menu[1] + c.MENU_FONT_SIZE), 2)  # Draw horizontal separator line
        # Draw menu text here using c.MENU_TEXT_COLOR and c.MENU_FONT_SIZE
        menu_font = pygame.font.SysFont(None, c.MENU_FONT_SIZE)
        value_font = pygame.font.SysFont(None, c.MENU_FONT_SIZE*2)
        marge = (10,10)
        
        # Draw Score
        score_text = menu_font.render(f"Score:", True, c.MENU_TEXT_COLOR)
        score_text_height = score_text.get_height() + 10 + marge[1]
        x = (c.GAME_WIDTH // 2 - score_text.get_width()) // 2
        self.screen.blit(score_text, (x, pos_menu[1] + marge[1]))

        score_value_text = value_font.render(f"{self.score}", True, c.CYAN)
        x = (c.GAME_WIDTH // 2 - score_value_text.get_width()) // 2
        y = pos_menu[1] + marge[1] + score_text.get_height() + 10
        score_space = c.MENU_HEIGHT - score_text_height
        y = pos_menu[1] + score_text_height + score_space // 2 - score_value_text.get_height() // 2
        self.screen.blit(score_value_text, (x, y))

        # Draw Snake Length
        length_text = menu_font.render(f"Length:", True, c.MENU_TEXT_COLOR)
        x = c.GAME_WIDTH // 2 + (c.GAME_WIDTH // 2 - length_text.get_width()) // 2
        self.screen.blit(length_text, (x, pos_menu[1] + marge[1]))

        length_value_text = value_font.render(f"{self.snake.get_size()}", True, c.CYAN)
        x = c.GAME_WIDTH // 2 + (c.GAME_WIDTH // 2 - length_value_text.get_width()) // 2
        y = pos_menu[1] + marge[1] + length_text.get_height() + 10
        length_space = c.MENU_HEIGHT - (length_text.get_height() + 10 + marge[1])
        y = pos_menu[1] + length_text.get_height() + 10 + marge[1] + length_space // 2 - length_value_text.get_height() // 2
        self.screen.blit(length_value_text, (x, y))

    def gameover_screen(self): 
        gameover_font = pygame.font.SysFont(None, c.MENU_FONT_SIZE*2)
        gameover_text = gameover_font.render("Game Over!", True, c.RED)
        x = (c.GAME_WIDTH - gameover_text.get_width()) // 2
        y = (c.GAME_HEIGHT - gameover_text.get_height()) // 2
        self.screen.blit(gameover_text, (x, y))
        pygame.display.flip()  # Update the display to show the game over message
        print("Game Over! Thanks for playing.")
        self.gameover = True  # Set game over flag