class SnakeAgent:
    def __init__(self, env, agent):
        self.env = env
        self.agent = agent

    def get_state(self):
        head_x, head_y = self.env.snake.body[0]
        vision_grid = self.env.vision(self.env.fruits)
        up_string = "".join(vision_grid[i][head_x + 1]
                            for i in range(head_y + 1))
        down_string = "".join(vision_grid[i][head_x + 1]
                              for i in range(head_y + 2, len(vision_grid)))
        left_string = "".join(vision_grid[head_y + 1][i]
                              for i in range(head_x + 1))
        right_string = "".join(vision_grid[head_y + 1][i]
                               for i in range(head_x + 2, len(vision_grid[0])))

        def is_dangerous(char: str) -> bool:
            """Determines if a character in the vision grid
            represents a danger to the snake."""
            return (
                char == 'W' or
                char == 'S' or
                (char == 'R' and len(self.env.snake.body) <= 2)
            )

        # Immediate Danger in each direction
        danger = (
            is_dangerous(up_string[0]),
            is_dangerous(down_string[0]),
            is_dangerous(left_string[0]),
            is_dangerous(right_string[0]),
        )

        # First object seen on the path
        def scan(string: str) -> str:
            """Iterates through the squares in order and returns
            whatever is seen first: 'W', 'G', 'R'.

            The snake's body is treated as a wall
            to minimize the number of states.
            """
            for char in string:
                if is_dangerous(char):
                    return 'W'  # Wall, Body or Dangerous Red Apple
                if char == 'G' or char == 'R':
                    return char
            return 'W'

        up = scan(up_string)
        down = scan(down_string)
        left = scan(left_string)
        right = scan(right_string)

        return (
            danger,
            self.env.snake.direction,
            up, down, right, left,  # 'W' | 'G' | 'R'
        )

    def train(self, episodes: int):
        for episode in range(episodes):
            self.env.reset()
            state = self.get_state()
            done = False

            while not done:
                action = self.agent.choose_action(state)

                reward, done = self.env.step(action)
                if not done:
                    next_state = self.get_state()
                else:
                    next_state = state

                self.agent.learn(
                    state,
                    action,
                    reward,
                    next_state,
                    done
                )

                state = next_state

            self.agent.decay_epsilon()
        self.agent.save_model(episodes)

    def learn_step(self, state):
        action = self.agent.choose_action(state)
        reward, done = self.env.step(action)
        if not done:
            next_state = self.get_state()
        else:
            next_state = state
        self.agent.learn(
            state,
            action,
            reward,
            next_state,
            done
        )
        if done:
            self.env.reset()

    def play(self):
        state = self.env.reset()
        done = False
        self.agent.load_model()

        while not done:
            action = self.agent.best_action(state)
            state, reward, done = self.env.step(action)

        print(f"Game over! Final score: {self.env.snake.score}")
