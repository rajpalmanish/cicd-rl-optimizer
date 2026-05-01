import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from env.cicd_env import CICDEnv

env = CICDEnv()

state, _ = env.reset()

print("Initial State:", state)

action = env.action_space.sample()

print("Random Action:", action)

next_state, reward, done, _, _ = env.step(action)

print("Next State:", next_state)
print("Reward:", reward)