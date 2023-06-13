import boto3
import os

session = boto3.Session(profile_name='sandbox')
s3 = session.client("s3")

sts_client = session.client('sts')
response = sts_client.get_caller_identity()
account_id = response['Account']
print("AccountID: ", account_id)

response = s3.list_buckets()
all_buckets = [bucket.get('Name') for bucket in response['Buckets']]
bucket_name = f'raw-car-dataset-{account_id}'

if bucket_name not in all_buckets:
    s3.create_bucket(
        ACL = 'private',
        Bucket = bucket_name
    )

cwd = os.getcwd()
s3.upload_file(Filename = cwd + f"\\data\\raw_data\\Automobile.csv",
               Bucket = bucket_name,
               Key = "Automobile.csv")