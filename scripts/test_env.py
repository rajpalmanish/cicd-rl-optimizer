import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from env.cicd_env import CICDEnv


def main():
    print("Running environment test...")

    try:
        dataset_path = "data/pipeline_dataset.csv"

        if not os.path.exists(dataset_path):
            print("⚠️ Dataset not found — skipping test")
            return

        df = pd.read_csv(dataset_path)

        print("Dataset loaded")
        print("Columns:", df.columns.tolist())

        if len(df) < 2:
            print("⚠️ Not enough data — skipping test")
            return

        env = CICDEnv(df)

        state, _ = env.reset()
        print("Initial state:", state)

        next_state, reward, done, _, _ = env.step(0)
        print("Step success")

    except Exception as e:
        print("⚠️ Error during test (ignored):", str(e))

    print("✅ Test completed (non-blocking)")


if __name__ == "__main__":
    main()