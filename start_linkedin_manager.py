#!/usr/bin/env python3
"""
Start the complete LinkedIn Post Manager with frontend and backend
"""
import subprocess
import time
import threading
import os

def start_fastapi():
    """Start FastAPI server"""
    os.chdir('/home/sagemaker-user/backend')
    subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"])

def start_localtunnel_fixed():
    """Start localtunnel with fixed subdomain"""
    # Install localtunnel if not present
    subprocess.run(["npm", "install", "-g", "localtunnel"], capture_output=True)
    
    # Use fixed subdomain
    subdomain = "mylinkedinapp"
    url = f"https://{subdomain}.loca.lt"
    
    # Start localtunnel with fixed subdomain
    process = subprocess.Popen(
        ["lt", "--port", "8001", "--subdomain", subdomain],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    return url, process

def main():
    print("🚀 Starting LinkedIn Post Manager...")
    print("=" * 50)
    
    # Start localtunnel
    tunnel_url, tunnel_process = start_localtunnel_fixed()
    
    print(f"📱 Frontend available at: {tunnel_url}")
    print(f"🔧 API available at: {tunnel_url}/api")
    print(f"🔗 LinkedIn OAuth redirect: {tunnel_url}/auth/callback")
    print("✅ URL stays the same on restart!")
    print("=" * 50)
    print("Starting servers...")
    
    # Start FastAPI in a separate thread
    server_thread = threading.Thread(target=start_fastapi, daemon=True)
    server_thread.start()
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\\n🛑 Shutting down...")
        tunnel_process.terminate()

if __name__ == "__main__":
    main()