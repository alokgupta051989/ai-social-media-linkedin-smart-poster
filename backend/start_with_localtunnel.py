#!/usr/bin/env python3
"""
Start FastAPI server with localtunnel (no auth required)
"""
import subprocess
import time
import threading
import requests
import json

def start_fastapi():
    """Start FastAPI server"""
    subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"])

def start_localtunnel():
    """Start localtunnel and return the URL"""
    # Install localtunnel if not present
    subprocess.run(["npm", "install", "-g", "localtunnel"], capture_output=True)
    
    # Start localtunnel
    process = subprocess.Popen(
        ["lt", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for URL
    for line in process.stdout:
        if "your url is:" in line:
            url = line.split("your url is: ")[1].strip()
            return url, process
    
    return None, process

def main():
    print("Starting localtunnel...")
    
    # Start localtunnel
    tunnel_url, tunnel_process = start_localtunnel()
    
    if tunnel_url:
        print(f"\n🚀 FastAPI server will be available at: {tunnel_url}")
        print(f"📋 Set LinkedIn redirect URI to: {tunnel_url}/auth/callback")
        print(f"🔗 OAuth authorization endpoint: {tunnel_url}/auth/linkedin")
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
            tunnel_process.terminate()
    else:
        print("Failed to start localtunnel")

if __name__ == "__main__":
    main()