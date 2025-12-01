# 🚀 START HERE - Simple Setup

## Quick Start (2 Steps)

### 1. Start the Server

Open PowerShell and run:
```powershell
cd server
.\start_server.ps1
```

**Wait until you see:**
```
✅ Server ready! Listening on http://localhost:5000
```

**Keep this window open!**

### 2. Start the Frontend

Open a **NEW** PowerShell window and run:
```powershell
npm run dev
```

**Wait until you see:**
```
➜  Local:   http://localhost:8080/
```

### 3. Use It!

1. Open your browser to `http://localhost:8080`
2. Click "Choose File"
3. Select any tree image
4. Get results!

## ✅ That's It!

You need **2 terminals running**:
- **Terminal 1**: Server on port 5000 (shows "Server ready!")
- **Terminal 2**: Frontend on port 8080 (shows "Local: http://localhost:8080/")

Both must stay open.

## 🐛 If Something Doesn't Work

1. **Test the server**: Open `http://localhost:5000/health` in your browser
   - Should show: `{"status":"ok","message":"Tree classification API is running"}`
   
2. **If blocked by ad blocker**: 
   - Disable ad blocker for localhost
   - Or try incognito/private window

3. **Server won't start?**
   - Make sure Python 3.12 is installed
   - Check that `train/model.keras` exists

## 📝 Ports

- **Frontend**: Port 8080 (Vite dev server)
- **Backend API**: Port 5000 (Flask server)

These are separate and won't conflict!
