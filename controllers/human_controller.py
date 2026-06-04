class HumanController:

    def __init__(self):
        pass

    def handle_event(self, event):

        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_UP:
            return UP

        if event.key == pygame.K_DOWN:
            return DOWN

        if event.key == pygame.K_LEFT:
            return LEFT

        if event.key == pygame.K_RIGHT:
            return RIGHT