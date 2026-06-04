class SnakeEnv:
    def __init__(self, nb_cells=20, initial_size=3):
        self.nb_cells = nb_cells
        self.initial_size = initial_size
        self.reset()

    def reset(self):
        self.snake = Snake(
            start_pos=(self.nb_cells // 2, self.nb_cells // 2),
            initial_size=self.initial_size,
        )
        self.score = 0
        self.game_over = False

    def step(self, action):
        pass

    def get_state(self):
        pass

    def spawn_fruit(self):
        pass

    def check_collision(self):
        pass