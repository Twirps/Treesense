# Quick Start Guide

## Step-by-Step Setup

### 1. Start the API Server

Open a **new terminal/PowerShell window** and run:

```powershell
cd C:\Users\MrKup\Github\treesense\server
.\start_server.ps1
```

**Wait for this message:**
```
✅ Server ready! Listening on http://localhost:8080
```

**Keep this terminal open!** The server must stay running.

### 2. Start the Frontend

Open a **different terminal/PowerShell window** and run:

```powershell
cd C:\Users\MrKup\Github\treesense
npm run dev
```

**Wait for this message:**
```
  VITE v5.x.x  ready in xxx ms
  ➜  Local:   http://localhost:5173/
```

### 3. Test the Server

Before uploading an image, test if the server is working:

Open in your browser: **http://localhost:8080/health**

You should see:
```json
{"status":"ok","message":"Tree classification API is running"}
```

### 4. Use the App

1. Open your browser to the frontend URL (usually `http://localhost:5173`)
2. Click "Choose File"
3. Select a tree image
4. Wait for results!

## Common Issues

### "Server not running"
- Make sure you ran `.\start_server.ps1` in the `server` folder
- Check that you see "Server ready!" message
- The server terminal must stay open

### "ERR_BLOCKED_BY_CLIENT"
- This is an ad blocker
- Try disabling your ad blocker for localhost
- Or test in an incognito/private window with extensions disabled

### "Cannot connect"
- Make sure BOTH server and frontend are running
- Check that server shows "Listening on http://localhost:8080"
- Try the health check URL in your browser first

## What Should Be Running

You should have **2 terminals open**:
1. **Server terminal** - showing Flask server logs
2. **Frontend terminal** - showing Vite dev server

Both must stay running!

