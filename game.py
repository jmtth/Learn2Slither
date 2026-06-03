import pygame
# from scenes.game_scene import GameScene
from scenes.mainmenu_scene import MainMenuScene
import const as c


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Learn2Slither Snake')
        self.screen = pygame.display.set_mode((c.SCREEN_SIZE[0], c.SCREEN_SIZE[1]))
        self.clock = pygame.time.Clock()
        self.running = True
        self.pause = True
        self.scene = MainMenuScene(self)

    def change_scene(self, scene):
        self.scene = scene

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.scene.handle_event(event)

            self.scene.update()
            self.scene.draw(self.screen)

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
