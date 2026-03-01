import boto3
from datetime import datetime
import json

s3 = boto3.client("s3")

def save_draft(topic: str, draft: str, bucket: str = "social-media-ai-agent-drafts"):
    """Save draft to S3"""
    timestamp = datetime.now().isoformat()
    key = f"drafts/{topic}_{timestamp}.txt"
    
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=draft
    )
    return key

def get_draft(key: str, bucket: str = "social-media-ai-agent-drafts"):
    """Retrieve draft from S3"""
    response = s3.get_object(Bucket=bucket, Key=key)
    return response['Body'].read().decode('utf-8')

def save_metadata(topic: str, metadata: dict, bucket: str = "social-media-ai-agent-drafts"):
    """Save post metadata to S3"""
    timestamp = datetime.now().isoformat()
    key = f"metadata/{topic}_{timestamp}.json"
    
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(metadata)
    )
    return key

def validate_topic(topic: str):
    """Basic topic validation"""
    if not topic or len(topic.strip()) == 0:
        return False, "Topic cannot be empty"
    if len(topic) > 100:
        return False, "Topic too long"
    return True, "Topic valid"