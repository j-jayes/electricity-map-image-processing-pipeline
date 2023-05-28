import boto3
import os
import yaml

def detect_text(bucket, key, region="us-east-1"):
    client = boto3.client('textract', region_name=region)

    response = client.detect_document_text(
        Document={'S3Object': {'Bucket': bucket, 'Name': key}})

    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            print('\033[94m' +  item["Text"] + '\033[0m')

# configure your AWS access key and secret access key
# either set them as environment variables or provide them explicitly
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# initialize boto3 session
session = boto3.Session(aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        region_name='us-east-1') # replace with your preferred region

# specify the S3 bucket you want to use
bucket_name = 'my_bucket'

s3_client = session.client('s3')

folder_path = "data/intermediate/stitched_images/"

# Upload each file in the directory
for file_name in os.listdir(folder_path):
    if file_name.endswith(".jpg") or file_name.endswith(".png"):
        # specify the full local path of the file
        local_file_path = os.path.join(folder_path, file_name)
        # specify the key in the s3 bucket - this will be the file's name
        s3_file_key = file_name
        # upload the file
        s3_client.upload_file(local_file_path, bucket_name, s3_file_key)
        # Run Textract on the uploaded image
        detect_text(bucket_name, s3_file_key)
