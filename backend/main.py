from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agent import generate_post, approve_post
from utils import save_draft, save_metadata, validate_topic
from linkedin import mock_linkedin_post, validate_post_content, get_access_token, post_to_linkedin, test_access_token, set_redirect_uri, CLIENT_ID
from datetime import datetime
import os

app = FastAPI(title="Social Media AI Agent", version="1.0.0")

# Set base URL for dynamic redirect URI
BASE_URL = None

@app.on_event("startup")
async def startup_event():
    # This will be set by the tunnel script
    pass

class Prompt(BaseModel):
    topic: str
    dry_run: bool = True
    access_token: str = None

class PostResponse(BaseModel):
    draft: str
    approved: bool
    saved_key: str = ""
    status: str

@app.get("/")
def root():
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"message": "Social Media AI Agent API", "status": "running"}

@app.get("/api")
def api_root():
    return {"message": "Social Media AI Agent API", "status": "running"}

@app.get("/auth/linkedin")
def get_linkedin_auth_url(request: Request, client_id: str = None, client_secret: str = None):
    """Get LinkedIn OAuth authorization URL"""
    # Get the base URL from the request
    base_url = f"{request.url.scheme}://{request.headers.get('host', request.url.netloc)}"
    set_redirect_uri(base_url)
    
    # Use custom credentials if provided, otherwise use default
    app_client_id = client_id if client_id else CLIENT_ID
    
    # Store custom credentials in session if provided
    if client_id and client_secret:
        # In a real app, you'd store this securely
        pass
    
    from linkedin import REDIRECT_URI
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?"
        f"response_type=code&"
        f"client_id={app_client_id}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"scope=openid%20profile%20w_member_social"
    )
    return {"auth_url": auth_url}

@app.post("/auth/test")
def test_token(request: dict):
    """Test access token validity"""
    access_token = request.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="access_token required")
    
    result = test_access_token(access_token)
    return result

@app.get("/auth/callback")
def linkedin_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "No code returned from LinkedIn"}
    
    # Exchange code for access token
    token_response = get_access_token(code)
    
    if "access_token" in token_response:
        return {
            "message": "Successfully authenticated with LinkedIn",
            "access_token": token_response["access_token"],
            "expires_in": token_response.get("expires_in", 5184000)
        }
    else:
        return {"error": "Failed to get access token", "details": token_response}

@app.post("/generate", response_model=PostResponse)
def generate_content(prompt: Prompt):
    # Validate topic
    valid, message = validate_topic(prompt.topic)
    if not valid:
        raise HTTPException(status_code=400, detail=message)
    
    # Generate content
    draft = generate_post(prompt.topic)
    
    # Approve content
    approved = approve_post(draft)
    
    # Validate post content
    content_valid, content_message = validate_post_content(draft)
    if not content_valid:
        approved = False
    
    # Save draft
    saved_key = save_draft(prompt.topic, draft)
    
    # Save metadata
    metadata = {
        "topic": prompt.topic,
        "generated_at": datetime.now().isoformat(),
        "approved": approved,
        "draft_key": saved_key
    }
    save_metadata(prompt.topic, metadata)
    
    return PostResponse(
        draft=draft,
        approved=approved,
        saved_key=saved_key,
        status="generated"
    )

@app.post("/publish")
def publish_post(prompt: Prompt):
    # Generate and validate content
    draft = generate_post(prompt.topic)
    approved = approve_post(draft)
    
    if not approved:
        raise HTTPException(status_code=400, detail="Content not approved for publishing")
    
    # Post to LinkedIn
    if prompt.access_token and not prompt.dry_run:
        # Real LinkedIn posting
        result = post_to_linkedin(draft, prompt.access_token)
        if "error" in result:
            raise HTTPException(status_code=400, detail=f"LinkedIn API error: {result['error']}")
    else:
        # Mock posting
        result = mock_linkedin_post(draft, prompt.dry_run)
    
    # Save metadata
    metadata = {
        "topic": prompt.topic,
        "published_at": datetime.now().isoformat(),
        "dry_run": prompt.dry_run,
        "result": result
    }
    save_metadata(prompt.topic, metadata)
    
    return {
        "status": "success",
        "draft": draft,
        "posted": not prompt.dry_run and prompt.access_token,
        "result": result
    }