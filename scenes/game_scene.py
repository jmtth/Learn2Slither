import const as c
import pygame
from scenes.scene import Scene
from render.game_render import GameRender
from game.snake_env import SnakeEnv
from controllers.human_controller import HumanController

# import game.snake_render as snake_render
# import game.apple as apple
# import scene.scene as scene


class GameScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        # self.board = pygame.Rect(0, 0, c.GAME_WIDTH, c.GAME_HEIGHT)
        # initial_position = self.app.config.snake_pos
        # self.snake = snake_render.Snake(initial_position)
        # self.fruits = [apple.Apple(c.RED), apple.Apple(c.GREEN), apple.Apple(c.GREEN)]
        self.gameover = False
        self.score = 0
        # self.snake_size = self.snake.get_size()  # Initialize snake size for score tracking
        self.pause = True
        # self.gamerender = Gamerender.Gamerender(self.game)
        self.env = SnakeEnv(app.config.game)
        # self.controller = HumanController(app.config.game)
        self.renderer = GameRender(app.config)

    # def run(self):
    #     while self.running:
    #         self.handle_events()
    #         if not self.gameover:
    #             self.snake.vision(self.fruits) # Get snake's vision of the environment
    #             if not self.pause:
    #                 self.update()
    #             self.draw()
    #         self.clock.tick(c.FPS)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pass
                # self.snake.change_direction((0, -1))
            elif event.key == pygame.K_DOWN:
                pass
                # self.snake.change_direction((0, 1))
            elif event.key == pygame.K_LEFT:
                pass
                # self.snake.change_direction((-1, 0))
            elif event.key == pygame.K_RIGHT:
                pass
                # self.snake.change_direction((1, 0))
            elif event.key == pygame.K_ESCAPE: 
                from scenes.mainmenu_scene import MainMenuScene
                self.app.change_scene(MainMenuScene(self.app))
                self.gameover = False
                # self.snake = snake_render.Snake((c.GAME_WIDTH // 2, c.GAME_HEIGHT // 2))
                # self.fruits = [apple.Apple(c.RED), apple.Apple(c.GREEN), apple.Apple(c.GREEN)]
                self.score = 0
                # self.snake_size = self.snake.get_size()  # Reset snake size for score
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
        # self.score += self.snake.move(self.fruits)  # Update snake position
        # if not self.board.contains(self.snake.rect) or self.snake.get_size() <= 0 or self.snake.body[0] in self.snake.body[1:]:
        #     self.gameover=True
        pass

    def draw(self, screen):
        self.renderer.draw(screen, self.env)
       



if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()