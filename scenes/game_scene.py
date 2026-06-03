import const as c
import pygame
# import game.snake_render as snake_render
# import game.apple as apple
# import scene.scene as scene


class GameScene(scene.Scene):
    def __init__(self, game):
        super().__init__(game)
        pygame.display.set_caption('Learn2Slither Snake')
        self.screen = pygame.display.set_mode((c.SCREEN_SIZE[0], c.SCREEN_SIZE[1]))
        self.clock = pygame.time.Clock()
        self.running = True
        self.board = pygame.Rect(0, 0, c.GAME_WIDTH, c.GAME_HEIGHT)
        initial_position = (c.GAME_WIDTH // 2, c.GAME_HEIGHT // 2)
        self.snake = snake_render.Snake(initial_position)
        self.fruits = [apple.Apple(c.RED), apple.Apple(c.GREEN), apple.Apple(c.GREEN)]
        self.gameover = False
        self.score = 0
        self.snake_size = self.snake.get_size()  # Initialize snake size for score tracking
        self.pause = True

    def run(self):
        while self.running:
            self.handle_events()
            if not self.gameover:
                self.snake.vision(self.fruits) # Get snake's vision of the environment
                if not self.pause:
                    self.update()
                self.draw()
            self.clock.tick(c.FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction((1, 0))
                elif event.key == pygame.K_ESCAPE: 
                    self.gameover = False
                    self.snake = snake_render.Snake((c.GAME_WIDTH // 2, c.GAME_HEIGHT // 2))
                    self.fruits = [apple.Apple(c.RED), apple.Apple(c.GREEN), apple.Apple(c.GREEN)]
                    self.score = 0
                    self.snake_size = self.snake.get_size()  # Reset snake size for score
                elif event.key == pygame.K_p:
                    self.pause = not self.pause


            # pressed = pygame.key.get_pressed()
            # if pressed[pygame.K_UP]:
            #     self.snake.change_direction((0, -1))
            # elif pressed[pygame.K_DOWN]:
            #     self.snake.change_direction((0, 1))
            # elif pressed[pygame.K_LEFT]:
            #     self.snake.change_direction((-1, 0))
            # elif pressed[pygame.K_RIGHT]:
            #     self.snake.change_direction((1, 0))
            # elif pressed[pygame.K_ESCAPE]:
            #     self.gameover= False
            #     self.snake = snake.Snake((c.GAME_WIDTH // 2, c.GAME_HEIGHT // 2))
            #     self.fruits = [apple.Apple(c.RED), apple.Apple(c.GREEN), apple.Apple(c.GREEN)]
            #     self.score = 0
            #     self.snake_size = self.snake.get_size()  # Reset snake size for score

    def update(self):
        self.score += self.snake.move(self.fruits)  # Update snake position
        if not self.board.contains(self.snake.rect) or self.snake.get_size() <= 0 or self.snake.body[0] in self.snake.body[1:]:
            self.gameover=True
        #pass

    def draw(self):
        self.screen.fill(c.BG_COLOR)  # Clear screen with background color
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
       



if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()