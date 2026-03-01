# FastAPI + ngrok Setup for LinkedIn OAuth

## Quick Start

1. **Start the server with ngrok tunnel:**
   ```bash
   cd backend
   python start_with_ngrok.py
   ```

2. **Copy the public URL** displayed in the terminal (e.g., `https://abcd1234.ngrok.io`)

3. **Update LinkedIn App Settings:**
   - Go to your LinkedIn Developer Console
   - Set redirect URI to: `https://abcd1234.ngrok.io/auth/callback`

4. **Test OAuth Flow:**
   - Visit: `https://abcd1234.ngrok.io/auth/linkedin`
   - Complete LinkedIn authorization
   - You'll be redirected back to your callback endpoint

## Alternative Manual Method

If you prefer to run components separately:

```bash
# Terminal 1: Start FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 2: Start ngrok tunnel
ngrok http 8000
```

## Endpoints

- `GET /` - Health check
- `GET /auth/linkedin` - Get LinkedIn OAuth URL
- `GET /auth/callback` - OAuth callback endpoint
- `POST /generate` - Generate social media content
- `POST /publish` - Publish content to LinkedIn

## Notes

- The ngrok URL changes each time you restart (unless you have a paid plan)
- Remember to update LinkedIn redirect URI whenever the URL changes
- Keep the terminal running to maintain the tunnel