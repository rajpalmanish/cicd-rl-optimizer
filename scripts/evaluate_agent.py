import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from env.cicd_env import CICDEnv
from stable_baselines3 import PPO

# load environment
env = CICDEnv()

# load trained agent
model = PPO.load("models/cicd_rl_agent")

state, _ = env.reset()

print("\nStarting evaluation...\n")

for i in range(10):

    action, _ = model.predict(state)

    next_state, reward, done, _, _ = env.step(action)

    print("Step:", i)
    print("State:", state)
    print("Chosen Action:", action)
    print("Reward:", reward)
    print("-----------------------------")

    state = next_state