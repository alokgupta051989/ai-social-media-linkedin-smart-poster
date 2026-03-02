#!/usr/bin/env python3
"""
LinkedIn Post Automation - Single Script Solution
Handles OAuth, token exchange, and posting
"""
import requests
import sys

def complete_linkedin_post(auth_code, custom_message=None):
    """Complete the full flow: code -> token -> post"""
    
    print("🔄 Step 2: Getting Access Token...")
    print("=" * 40)
    
    # Exchange code for token
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    token_payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": "https://dzd-cu5gczjwthq0rr.sagemaker.us-east-1.on.aws/proxy/8000/auth/callback",
        "client_id": "your_client_id",
        "client_secret": "your_client_secret"
    }
    
    try:
        token_response = requests.post(token_url, data=token_payload, 
                                    headers={"Content-Type": "application/x-www-form-urlencoded"})
        
        if token_response.status_code != 200:
            print(f"❌ Token exchange failed: {token_response.status_code}")
            print(f"Response: {token_response.text}")
            return False
            
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            print("❌ No access token received")
            print(f"Response: {token_data}")
            return False
            
        print("✅ Access token obtained!")
        print(f"🔑 Token: {access_token[:20]}...")
        
        print("\n🚀 Step 3: Making LinkedIn Post...")
        print("=" * 40)
        
        # Make the post
        topic = custom_message or "Successfully integrated LinkedIn API with my AI agent! 🤖 #AI #LinkedIn #Automation"
        
        post_payload = {
            "topic": topic,
            "dry_run": False,
            "access_token": access_token
        }
        
        post_response = requests.post("http://localhost:8000/publish", json=post_payload)
        
        if post_response.status_code == 200:
            post_data = post_response.json()
            
            if post_data.get("posted"):
                print("🎉 SUCCESS! Post published to LinkedIn!")
                print(f"📝 Content: {post_data.get('draft', '')[:150]}...")
                
                result = post_data.get('result', {})
                if result.get('success'):
                    print(f"✅ LinkedIn confirmed: {result.get('message', 'Posted successfully')}")
                
                return True
            else:
                print("❌ Post failed")
                print(f"Result: {post_data.get('result', {})}")
                return False
        else:
            print(f"❌ Post API error: {post_response.status_code}")
            print(f"Response: {post_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🤖 LinkedIn Post Automation")
    print("=" * 40)
    print("")
    print("STEP 1: Get LinkedIn Authorization")
    print("Copy this URL to your browser:")
    print("https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=78qml2o6hj9sqt&redirect_uri=https://dzd-cu5gczjwthq0rr.sagemaker.us-east-1.on.aws/proxy/8000/auth/callback&scope=profile%20w_member_social")
    print("")
    print("After authorization, copy the 'code' from the callback URL")
    print("")
    
    if len(sys.argv) < 2:
        print("STEP 2: Run this script with your authorization code:")
        print("python complete_linkedin_post.py YOUR_AUTHORIZATION_CODE [CUSTOM_MESSAGE]")
        print("")
        print("Example:")
        print("python complete_linkedin_post.py AQV8cN2... 'My LinkedIn post! 🚀'")
        sys.exit(1)
    
    auth_code = sys.argv[1]
    custom_message = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = complete_linkedin_post(auth_code, custom_message)
    
    if success:
        print("\n🎉 SUCCESS! Your post is live on LinkedIn!")
    else:
        print("\n❌ Failed. Check error messages above.")