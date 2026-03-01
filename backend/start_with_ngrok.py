#!/usr/bin/env python3
"""
Start FastAPI server with ngrok tunnel for LinkedIn OAuth callback
"""
import subprocess
import time
from pyngrok import ngrok
import threading

def start_fastapi():
    """Start FastAPI server"""
    subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"])

def main():
    # Start ngrok tunnel
    print("Starting ngrok tunnel...")
    tunnel = ngrok.connect(8000)
    public_url = tunnel.public_url
    
    print(f"\n🚀 FastAPI server will be available at: {public_url}")
    print(f"📋 Set LinkedIn redirect URI to: {public_url}/auth/callback")
    print(f"🔗 OAuth authorization endpoint: {public_url}/auth/linkedin")
    print("\nStarting FastAPI server...")
    
    # Start FastAPI in a separate thread
    server_thread = threading.Thread(target=start_fastapi, daemon=True)
    server_thread.start()
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        ngrok.disconnect(tunnel.public_url)
        ngrok.kill()

if __name__ == "__main__":
    main()