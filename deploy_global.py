#!/usr/bin/env python3
"""
Deploy LinkedIn Post Manager globally using ngrok
"""
import subprocess
import time
import threading
import os

def start_fastapi():
    """Start FastAPI server"""
    os.chdir('/home/sagemaker-user/backend')
    subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"])

def start_ngrok():
    """Start ngrok tunnel"""
    # Start ngrok
    process = subprocess.Popen(
        ["ngrok", "http", "8002"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for ngrok to start
    time.sleep(3)
    
    # Get the public URL
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:4040/api/tunnels"],
            capture_output=True,
            text=True
        )
        import json
        data = json.loads(result.stdout)
        public_url = data['tunnels'][0]['public_url']
        return public_url, process
    except:
        return "Check ngrok dashboard at http://localhost:4040", process

def main():
    print("🌍 Deploying LinkedIn Post Manager globally...")
    print("=" * 50)
    
    # Start ngrok
    public_url, ngrok_process = start_ngrok()
    
    print(f"🚀 App available globally at: {public_url}")
    print(f"📱 Frontend: {public_url}")
    print(f"🔧 API: {public_url}/api")
    print(f"🔗 LinkedIn OAuth: {public_url}/auth/callback")
    print("🌐 Accessible from anywhere in the world!")
    print("=" * 50)
    
    # Start FastAPI
    server_thread = threading.Thread(target=start_fastapi, daemon=True)
    server_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        ngrok_process.terminate()

if __name__ == "__main__":
    main()