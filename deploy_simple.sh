#!/bin/bash

echo "🚀 Starting LinkedIn Post Manager..."

# Kill any existing processes
pkill -f uvicorn 2>/dev/null
pkill -f ngrok 2>/dev/null

# Start backend in background
cd /home/sagemaker-user/backend
uvicorn main:app --host 0.0.0.0 --port 8002 &
BACKEND_PID=$!

echo "⏳ Starting backend server..."
sleep 3

# Start ngrok tunnel
echo "🌍 Creating global tunnel..."
ngrok http 8002 &
NGROK_PID=$!

echo "⏳ Waiting for ngrok to start..."
sleep 5

# Get the public URL
echo "🔍 Getting public URL..."
PUBLIC_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if data.get('tunnels'):
        print(data['tunnels'][0]['public_url'])
    else:
        print('No tunnels found')
except:
    print('Dashboard not ready yet')
" 2>/dev/null)

if [ "$PUBLIC_URL" = "No tunnels found" ] || [ "$PUBLIC_URL" = "Dashboard not ready yet" ] || [ -z "$PUBLIC_URL" ]; then
    echo "📋 Check ngrok dashboard manually:"
    echo "   Open: http://localhost:4040"
    echo "   Or visit: https://dashboard.ngrok.com/tunnels/agents"
else
    echo "=================================="
    echo "🎉 SUCCESS! App deployed globally!"
    echo "🌍 Public URL: $PUBLIC_URL"
    echo "📱 Access from anywhere!"
    echo "=================================="
fi

echo ""
echo "✅ Backend running on port 8002"
echo "✅ ngrok tunnel active"
echo "📊 Dashboard: http://localhost:4040"
echo ""
echo "Press Ctrl+C to stop..."

# Keep running
wait $BACKEND_PID