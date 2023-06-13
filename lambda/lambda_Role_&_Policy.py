import boto3
import json

session = boto3.session.Session(profile_name='sandbox')

client = session.client("iam")
s3 = session.client("s3")

response = s3.list_buckets()
all_buckets = [bucket.get('Name') for bucket in response['Buckets']]

bucket_name = ''
for bucket in all_buckets:
    if bucket.startswith('raw-car-dataset-'):
        bucket_name = bucket
print("bucket: ", bucket_name)

# Creating 'LambdaS3CloudWatchRole' role
trust_policy = {
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "Statement1",
			"Effect": "Allow",
			"Principal": {
				"Service": "lambda.amazonaws.com"
			},
			"Action": "sts:AssumeRole"
		}
	]
}

role_name = 'LambdaS3CloudWatchRole'
client.create_role(
    RoleName = role_name,
    AssumeRolePolicyDocument = json.dumps(trust_policy), 
)

# Creating policy document and insering to 'LambdaS3CloudWatchRole' role
policy_document = {
    "Version": "2012-10-17",
    "Statement": [
         {
            "Effect":"Allow",

            "Action":[
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource":[
                "arn:aws:logs:us-east-1:*:*"
            ]
        },
        {
            "Effect": "Allow",

            "Action": [
                "s3:*"        
            ],
            "Resource": [                
                "arn:aws:s3:::*"
            ]
        }
    ]
}

policy_document_json = json.dumps(policy_document)
policy_response = client.put_role_policy(
    RoleName= role_name,
    PolicyName='LambdaS3CloudWatchPolicy',
    PolicyDocument=policy_document_json
)