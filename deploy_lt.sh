#!/bin/bash

echo "🚀 Starting LinkedIn Post Manager with localtunnel..."

# Kill existing processes
pkill -f uvicorn 2>/dev/null
pkill -f lt 2>/dev/null

# Install localtunnel
npm install -g localtunnel

# Start backend
cd /home/sagemaker-user/backend
uvicorn main:app --host 0.0.0.0 --port 8002 &

echo "⏳ Starting backend..."
sleep 3

# Start localtunnel
echo "🌍 Creating tunnel..."
lt --port 8002 --subdomain mylinkedinapp &

sleep 3

echo "=================================="
echo "🎉 App deployed globally!"
echo "🌍 Public URL: https://mylinkedinapp.loca.lt"
echo "📱 Access from anywhere!"
echo "=================================="

wait