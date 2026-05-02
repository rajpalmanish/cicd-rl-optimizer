import sys
import os

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from stable_baselines3 import PPO
from env.cicd_env import CICDEnv

# Paths
DATA_PATH = "data/pipeline_dataset.csv"
MODEL_PATH = "models/cicd_rl_agent.zip"


def preprocess_data(df):
    """
    Clean and prepare dataset for RL training
    """

    required_cols = [
        "commit_size",
        "files_changed",
        "compute_type",
        "build_time",
        "reward"
    ]

    # Check missing columns
    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        print(f"❌ Missing columns: {missing}")
        print("➡️ Run pipeline again to generate proper logs")
        return None

    # Convert types safely
    df["commit_size"] = pd.to_numeric(df["commit_size"], errors="coerce")
    df["files_changed"] = pd.to_numeric(df["files_changed"], errors="coerce")
    df["build_time"] = pd.to_numeric(df["build_time"], errors="coerce")
    df["reward"] = pd.to_numeric(df["reward"], errors="coerce")

    # Drop invalid rows
    df = df.dropna(subset=required_cols)

    # Map compute_type → action index
    action_map = {
        "BUILD_GENERAL1_SMALL": 0,
        "BUILD_GENERAL1_MEDIUM": 1,
        "BUILD_GENERAL1_LARGE": 2
    }

    df["action"] = df["compute_type"].map(action_map)

    # Drop rows where mapping failed
    df = df.dropna(subset=["action"])

    df["action"] = df["action"].astype(int)

    print(f"✅ Clean dataset size: {len(df)}")

    return df


def train():
    print("📥 Loading dataset...")

    if not os.path.exists(DATA_PATH):
        print("❌ Dataset not found. Run collect_from_s3.py first.")
        return

    df = pd.read_csv(DATA_PATH)

    df = preprocess_data(df)

    if df is None or len(df) == 0:
        print("❌ No valid data available for training.")
        return

    print("🧠 Creating environment...")
    env = CICDEnv(df)

    print("⚙️ Loading or creating model...")

    if os.path.exists(MODEL_PATH):
        print("🔄 Loading existing model...")
        model = PPO.load(MODEL_PATH, env=env)
    else:
        print("🆕 Creating new model...")
        model = PPO("MlpPolicy", env, verbose=1)

    print("🚀 Training model...")

    model.learn(total_timesteps=5000)

    print("💾 Saving model...")
    os.makedirs("models", exist_ok=True)
    model.save(MODEL_PATH)

    print("✅ Model training complete!")


if __name__ == "__main__":
    train()