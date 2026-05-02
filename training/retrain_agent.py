import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from stable_baselines3 import PPO
from env.cicd_env import CICDEnv

DATA_PATH = "data/pipeline_dataset.csv"
MODEL_PATH = "models/cicd_rl_agent.zip"

def train():

    df = pd.read_csv(DATA_PATH)

    # Ensure clean data
    df = df.dropna(subset=[
        "commit_size",
        "files_changed",
        "build_time",
        "reward",
        "compute_type"
    ])

    env = CICDEnv(df)

    # Load existing model OR create new
    if os.path.exists(MODEL_PATH):
        print("Loading existing model...")
        model = PPO.load(MODEL_PATH, env=env)
    else:
        print("Creating new model...")
        model = PPO("MlpPolicy", env, verbose=1)

    # Train
    model.learn(total_timesteps=5000)

    # Save model
    model.save(MODEL_PATH)

    print("✅ Model updated")


if __name__ == "__main__":
    train()