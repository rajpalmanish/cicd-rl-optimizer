import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random


class CICDEnv(gym.Env):

    def __init__(self):
        super(CICDEnv, self).__init__()

        # STATE SPACE
        # commit_size (0–500)
        # files_changed (0–50)
        self.observation_space = spaces.Box(
            low=np.array([0, 0]),
            high=np.array([500, 50]),
            dtype=np.float32
        )

        # ACTION SPACE
        # 0 = small compute
        # 1 = medium compute
        # 2 = large compute
        self.action_space = spaces.Discrete(3)

    def reset(self, seed=None):

        commit_size = random.randint(10, 500)
        files_changed = random.randint(1, 20)

        state = np.array([commit_size, files_changed], dtype=np.float32)

        return state, {}

    def step(self, action):

        commit_size = random.randint(10, 500)

        # simulate compute behaviour
        if action == 0:  # small compute
            build_time = commit_size * 0.6
            cost = 0.3

        elif action == 1:  # medium compute
            build_time = commit_size * 0.4
            cost = 0.5

        else:  # large compute
            build_time = commit_size * 0.2
            cost = 0.8

        reward = -(build_time + cost)

        done = True

        next_state = np.array([
            random.randint(10, 500),
            random.randint(1, 20)
        ], dtype=np.float32)

        return next_state, reward, done, False, {}