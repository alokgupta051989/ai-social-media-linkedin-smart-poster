# LinkedIn AI Agent - Production Ready

## Quick Start

1. **Start the server:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Make a LinkedIn post:**
   ```bash
   python complete_linkedin_post.py
   ```
   This will show you the OAuth URL. After authorization, run:
   ```bash
   python complete_linkedin_post.py YOUR_AUTH_CODE "Your message here!"
   ```

## Files:
- `main.py` - FastAPI server with LinkedIn integration
- `linkedin.py` - LinkedIn API functions
- `agent.py` - AI content generation (AWS Bedrock)
- `utils.py` - Utility functions
- `complete_linkedin_post.py` - **Main script for posting**
- `requirements.txt` - Dependencies

## OAuth URL:
```
https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=78qml2o6hj9sqt&redirect_uri=https://dzd-cu5gczjwthq0rr.sagemaker.us-east-1.on.aws/proxy/8000/auth/callback&scope=profile%20w_member_social
```

That's it! 🚀