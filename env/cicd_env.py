import gymnasium as gym
from gymnasium import spaces
import numpy as np


class CICDEnv(gym.Env):

    def __init__(self, df):
        super(CICDEnv, self).__init__()

        # Dataset (real pipeline data)
        self.df = df.reset_index(drop=True)
        self.current_step = 0

        # STATE SPACE
        # commit_size, files_changed
        self.observation_space = spaces.Box(
            low=np.array([0, 0]),
            high=np.array([10000, 100]),
            dtype=np.float32
        )

        # ACTION SPACE
        # 0 = SMALL, 1 = MEDIUM, 2 = LARGE
        self.action_space = spaces.Discrete(3)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.current_step = 0
        return self._get_state(), {}

    def _get_state(self):
        row = self.df.iloc[self.current_step]

        state = np.array([
            row["commit_size"],
            row["files_changed"]
        ], dtype=np.float32)

        return state

    def step(self, action):

        row = self.df.iloc[self.current_step]

        # Expected correct action from dataset
        expected_action = row["action"]

        # Reward from dataset (already computed)
        reward = row["reward"]

        # Optional: Penalize wrong action (helps learning)
        if action != expected_action:
            reward -= 5

        # Move to next step
        self.current_step += 1

        done = self.current_step >= len(self.df) - 1

        if not done:
            next_state = self._get_state()
        else:
            next_state = np.zeros(2, dtype=np.float32)

        return next_state, reward, done, False, {}