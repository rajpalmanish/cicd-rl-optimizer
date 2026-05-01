import sys
import os

# allow imports from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from env.cicd_env import CICDEnv
from stable_baselines3 import PPO

# create environment
env = CICDEnv()

# create PPO agent
model = PPO(
    "MlpPolicy",
    env,
    verbose=1
)

# train the agent
model.learn(total_timesteps=10000)

# save trained model
model.save("models/cicd_rl_agent")

print("Training complete. Model saved.")