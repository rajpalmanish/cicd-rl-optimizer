import csv
import os
import random
import time
import boto3

# Placeholder for CloudWatch integration
# Future: fetch build logs from AWS
# dataset location
DATA_FILE = "data/pipeline_dataset.csv"

# create dataset if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "commit_size",
            "files_changed",
            "instance_type",
            "build_time",
            "cost",
            "success"
        ])

# simulate pipeline metrics (temporary for now)
commit_size = random.randint(10, 500)
files_changed = random.randint(1, 20)

instance_type = random.choice(["small", "medium", "large"])

build_time = random.randint(20, 120)

# simple cost estimation
cost_per_second = 0.00001
cost = build_time * cost_per_second

success = random.choice([0, 1])

# write data row
with open(DATA_FILE, "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        commit_size,
        files_changed,
        instance_type,
        build_time,
        cost,
        success
    ])

print("Pipeline run recorded:")
print({
    "commit_size": commit_size,
    "files_changed": files_changed,
    "instance_type": instance_type,
    "build_time": build_time,
    "cost": cost,
    "success": success
})