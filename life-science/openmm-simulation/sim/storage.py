import os
import subprocess
from pathlib import Path

try:
    import boto3
    from botocore.config import Config
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False


def configure_aws_cli():
    """Configure AWS CLI with environment variables."""
    try:
        # Get environment variables
        region = os.environ.get('AWS_DEFAULT_REGION', 'eu-north1')
        endpoint_url = os.environ.get('S3_ENDPOINT_URL', 'https://storage.eu-north1.nebius.cloud:443')
        
        # Configure AWS CLI
        subprocess.run(['aws', 'configure', 'set', 'region', region], check=True)
        subprocess.run(['aws', 'configure', 'set', 'endpoint_url', endpoint_url], check=True)
        
        print(f"Configured AWS CLI: region={region}, endpoint={endpoint_url}")
        return True
    except Exception as e:
        print(f"Failed to configure AWS CLI: {e}")
        return False
        
def check_s3_configuration() -> bool:
    """Check if S3 is properly configured."""

    if not BOTO3_AVAILABLE:
        print("Warning: boto3 not available. S3 upload will be skipped.")
        return False
        
    required_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"Missing S3 configuration: {', '.join(missing_vars)}")
        return False

    # Configure AWS CLI first
    if not configure_aws_cli():
        print("Failed to configure AWS CLI, trying with boto3 directly...")
    
    return True

def upload_results_to_s3(sim_dir: Path) -> bool:
    """Upload all simulation results to S3."""

    if not check_s3_configuration():
        print("S3 configuration is not set. Skipping upload.")
        return False

    try:
        bucket_name = os.environ.get('S3_BUCKET')
        s3_prefix = os.environ.get('S3_PREFIX', '')
        s3_endpoint_url = os.environ.get('S3_ENDPOINT_URL')
        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        aws_default_region = os.environ.get('AWS_DEFAULT_REGION')

        # Configure boto3 with the custom endpoint URL
        s3_config = Config(region_name=aws_default_region)
        s3_client = boto3.client(
            's3',
            config=s3_config,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=s3_endpoint_url
        )

        print("="*50)
        print(f"Uploading to S3: {bucket_name}")
        print(f"Endpoint: {s3_endpoint_url}")
        # Test bucket access first
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            print(f"Successfully connected to bucket: {bucket_name}")
        except Exception as e:
            print(f"Cannot access bucket {bucket_name}: {e}")
            return False
        
        # Upload all files in the simulation directory recursively
        uploaded_files = []
        for file_path in sim_dir.rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(sim_dir).as_posix()
                s3_key = f"{s3_prefix}/{sim_dir.name}/{relative_path}"
                s3_client.upload_file(str(file_path), bucket_name, s3_key)
                uploaded_files.append(relative_path)
                print(f"Uploaded {relative_path} to S3: s3://{bucket_name}/{s3_key}")
        
        print(f"Successfully uploaded {len(uploaded_files)} files to S3")
        return True
        
    except Exception as e:
        print(f"Failed to upload to S3: {e}")
        return False

