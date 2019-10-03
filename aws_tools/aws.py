import boto3


class AwsS3Utils:
    s3client = None

    def __init__(self, bucket_name=None, aws_access_key_id=None, aws_secret_access_key=None):
        self.bucket_name = bucket_name
        if aws_access_key_id and aws_secret_access_key:
            self.s3client = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                                         aws_secret_access_key=aws_secret_access_key)
        else:
            self.s3client = boto3.client('s3')

    def create_bucket(self, bucket_name=None):
        self.bucket_name = bucket_name or self.bucket_name
        if self.bucket_name:
            print('Creating new bucket with name: {}'.format(bucket_name))
            self.s3client.create_bucket(Bucket=bucket_name)
        else:
            raise Exception("empty bucket name given")

    def get_all_buckets_details(self):
        list_buckets_resp = self.s3client.list_buckets()
        for bucket in list_buckets_resp['Buckets']:
            print('(Just created) --> {} - there since {}'.format(
                bucket['Name'], bucket['CreationDate']))

    def upload_file(self, file_path_to_upload, path_to_upload_to, bucket_name=None):
        bucket_name = bucket_name or self.bucket_name
        print('Uploading some data to {} with key: {}'.format(
            bucket_name, path_to_upload_to))
        with open(file_path_to_upload, 'r') as file_to_upload:
            self.s3client.put_object(Bucket=bucket_name, Key=path_to_upload_to, Body=file_to_upload.read())

