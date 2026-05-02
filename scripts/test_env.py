import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from env.cicd_env import CICDEnv


def main():
    print("Testing environment...")

    # Load dataset
    dataset_path = "data/pipeline_dataset.csv"

    if not os.path.exists(dataset_path):
        print("❌ Dataset not found")
        return

    df = pd.read_csv(dataset_path)

    if len(df) < 2:
        print("⚠️ Not enough data for environment")
        return

    env = CICDEnv(df)

    state, _ = env.reset()

    print("Initial state:", state)

    next_state, reward, done, _, _ = env.step(0)

    print("Next state:", next_state)
    print("Reward:", reward)

    print("✅ Environment test passed")


if __name__ == "__main__":
    main()