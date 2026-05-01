import boto3

s3 = boto3.client('s3')

bucket = "cicd-rl-system-manish"
key = "data/pipeline_dataset.csv"

obj = s3.get_object(Bucket=bucket, Key=key)

data = obj['Body'].read().decode('utf-8')

print(data[:200])