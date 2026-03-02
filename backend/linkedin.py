import requests
import os

# LinkedIn OAuth credentials
CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "your_client_id")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "your_client_secret")

# Dynamic redirect URI - will be set by the server
REDIRECT_URI = None

def set_redirect_uri(base_url: str):
    """Set the redirect URI dynamically"""
    global REDIRECT_URI
    REDIRECT_URI = f"{base_url}/auth/callback"

def get_access_token(auth_code: str):
    """Exchange authorization code for access token"""
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(url, data=payload, headers=headers)
    return resp.json()

def test_access_token(access_token: str):
    """Test access token and check permissions"""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Test profile access
    profile_url = "https://api.linkedin.com/v2/userinfo"
    profile_resp = requests.get(profile_url, headers=headers)
    
    result = {
        "valid": profile_resp.status_code == 200,
        "profile_access": {
            "status_code": profile_resp.status_code,
            "success": profile_resp.status_code == 200
        }
    }
    
    if profile_resp.status_code == 200:
        try:
            result["profile_data"] = profile_resp.json()
        except:
            result["profile_data"] = profile_resp.text
    else:
        result["profile_error"] = profile_resp.text
    
    return result

def post_to_linkedin(content: str, access_token: str):
    """Post content to LinkedIn using API"""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    # Get user profile ID using newer API
    profile_url = "https://api.linkedin.com/v2/userinfo"
    profile_resp = requests.get(profile_url, headers=headers)
    
    if profile_resp.status_code != 200:
        return {
            "error": "Failed to get user profile", 
            "status_code": profile_resp.status_code,
            "details": profile_resp.text
        }
    
    profile_data = profile_resp.json()
    user_id = profile_data.get("sub")
    
    if not user_id:
        return {"error": "Could not extract user ID", "profile_data": profile_data}
    
    # Use newer posts API
    post_url = "https://api.linkedin.com/v2/posts"
    
    body = {
        "author": f"urn:li:person:{user_id}",
        "commentary": content,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED"
    }
    
    print(f"Posting to LinkedIn with body: {body}")
    resp = requests.post(post_url, json=body, headers=headers)
    
    result = {
        "status_code": resp.status_code,
        "response": resp.text,
        "request_body": body
    }
    
    try:
        result["json"] = resp.json()
    except:
        pass
        
    if resp.status_code == 201:
        result["success"] = True
        result["message"] = "Post created successfully"
    else:
        result["success"] = False
        result["error"] = f"API returned {resp.status_code}"
        print(f"LinkedIn API Error: {resp.status_code} - {resp.text}")
    
    return result

def mock_linkedin_post(content: str, dry_run: bool = True):
    """Mock LinkedIn posting function"""
    if dry_run:
        print("=== MOCK LINKEDIN POST ===")
        print(content)
        print("=== END MOCK POST ===")
        return {"status": "success", "posted": False, "message": "Dry run completed"}
    else:
        print("=== WOULD POST TO LINKEDIN ===")
        print(content)
        return {"status": "success", "posted": True, "message": "Posted to LinkedIn"}

def validate_post_content(content: str):
    """Basic content validation"""
    if len(content) > 3000:
        return False, "Content too long for LinkedIn"
    if len(content) < 10:
        return False, "Content too short"
    return True, "Content valid"