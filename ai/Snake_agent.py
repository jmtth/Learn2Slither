class SnakeAgent:
    def __init__(self, env, agent):
        self.env = env
        self.agent = agent

    def train(self, episodes: int):
        for episode in range(episodes):
            state = self.env.reset()
            done = False

            while not done:
                action = self.agent.choose_action(state)

                next_state, reward, done = self.env.step(action)

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
        next_state, reward, done = self.env.step(action)
        self.agent.learn(
            state,
            action,
            reward,
            next_state,
            done
        )
        state = next_state
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
