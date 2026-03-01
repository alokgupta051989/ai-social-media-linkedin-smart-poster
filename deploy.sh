#!/bin/bash

echo "🚀 Deploying LinkedIn Post Manager globally..."

# Install ngrok if not present
if ! command -v ngrok &> /dev/null; then
    echo "Installing ngrok..."
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
    sudo apt update && sudo apt install ngrok
fi

# Start backend
cd backend
uvicorn main:app --host 0.0.0.0 --port 8001 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start ngrok tunnel
ngrok http 8001 --log=stdout &
NGROK_PID=$!

# Wait for ngrok to start
sleep 5

# Get public URL
PUBLIC_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])")

echo "=================================="
echo "🌍 App deployed globally!"
echo "📱 Access from anywhere: $PUBLIC_URL"
echo "🔗 Share this URL with anyone!"
echo "=================================="

# Keep running
wait $BACKEND_PID