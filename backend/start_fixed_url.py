#!/usr/bin/env python3
"""
Start FastAPI server with fixed localtunnel subdomain
"""
import subprocess
import time
import threading

def start_fastapi():
    """Start FastAPI server"""
    subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"])

def start_localtunnel_fixed():
    """Start localtunnel with fixed subdomain"""
    # Install localtunnel if not present
    subprocess.run(["npm", "install", "-g", "localtunnel"], capture_output=True)
    
    # Use fixed subdomain
    subdomain = "mylinkedinapp"
    url = f"https://{subdomain}.loca.lt"
    
    # Start localtunnel with fixed subdomain
    process = subprocess.Popen(
        ["lt", "--port", "8000", "--subdomain", subdomain],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    return url, process

def main():
    print("Starting localtunnel with FIXED subdomain...")
    
    # Start localtunnel
    tunnel_url, tunnel_process = start_localtunnel_fixed()
    
    print(f"\n🚀 FastAPI server will be available at: {tunnel_url}")
    print(f"📋 Set LinkedIn redirect URI to: {tunnel_url}/auth/callback")
    print(f"🔗 OAuth authorization endpoint: {tunnel_url}/auth/linkedin")
    print("✅ URL will stay the same on restart!")
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

if __name__ == "__main__":
    main()