import boto3
import pandas as pd

# CONFIG
BUCKET_NAME = "cicd-rl-system-manish"   # <-- change this
PREFIX = "logs/"

s3 = boto3.client('s3')

def parse_file(content):
    record = {}

    for line in content.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            record[key.strip()] = value.strip()

    return record


def estimate_cost(build_time, compute_type):
    cost_map = {
        "BUILD_GENERAL1_SMALL": 1,
        "BUILD_GENERAL1_MEDIUM": 2,
        "BUILD_GENERAL1_LARGE": 4
    }
    return build_time * cost_map.get(compute_type, 1)


def calculate_reward(build_time, cost, success):
    failure_penalty = 0 if int(success) == 1 else 100
    reward = -(0.6 * build_time + 0.3 * cost + 0.1 * failure_penalty)
    return reward


def main():
    objects = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)

    data = []

    for obj in objects.get('Contents', []):
        key = obj['Key']

        if key.endswith(".txt"):
            file = s3.get_object(Bucket=BUCKET_NAME, Key=key)
            content = file['Body'].read().decode('utf-8')

            record = parse_file(content)

            try:
                # Convert types
                build_time = int(record.get("build_time", 0))
                success = int(record.get("BUILD_STATUS", 0))
                compute_type = record.get("compute_type", "BUILD_GENERAL1_SMALL")

                # Calculate cost + reward
                cost = estimate_cost(build_time, compute_type)
                reward = calculate_reward(build_time, cost, success)

                # Add computed fields
                record["cost"] = cost
                record["reward"] = reward

                data.append(record)

            except Exception as e:
                print(f"Skipping record due to error: {e}")

    # Create DataFrame
    df = pd.DataFrame(data)

    # Save locally
    df.to_csv("data/pipeline_dataset.csv", index=False)

    print("✅ Dataset created with", len(df), "records")


if __name__ == "__main__":
    main()