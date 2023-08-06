def add_profile():
    pass

def edit_profile():
    pass

def get_aws_session(**kwargs):
    import sys
    import boto3
    from botocore.exceptions import ProfileNotFound
    try:
        aws_session = boto3.session.Session(**kwargs)
    except ProfileNotFound:
        print(f"Profile not found.Please specify correct profile")
        sys.exit(1)
    return aws_session

def get_aws_client(aws_session, service, region=None, **kwargs):
    from botocore.exceptions import NoRegionError , NoCredentialsError 
    aws_client = aws_session.client(service, region, **kwargs)
    return aws_client
