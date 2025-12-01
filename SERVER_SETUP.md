# Server-Side API Setup Guide

## ✅ What Changed

The frontend now uses a **server-side API** instead of TensorFlow.js in the browser. This completely eliminates the browser compilation freeze issue!

## 🚀 Quick Start

### Step 1: Start the API Server

**Windows PowerShell (recommended):**
```powershell
cd server
.\start_server.ps1
```

**Or use the batch file:**
```powershell
cd server
.\start_server.bat
```

**Manual:**
```bash
cd server
python app.py
```

You should see:
```
🚀 Starting Tree Classification API Server...
✅ Model loaded! Input shape: (None, 160, 160, 3)
✅ Class mapping loaded: 10 classes
✅ Server ready! Listening on http://localhost:8080
```

### Step 2: Start the Frontend

In a **separate terminal**:
```bash
npm run dev
```

### Step 3: Test It!

1. Open your browser to the frontend (usually `http://localhost:5173`)
2. Upload an image
3. It should work instantly - no freezing! 🎉

## 📁 Files Created

- `server/app.py` - Flask API server
- `server/requirements.txt` - Python dependencies
- `server/start_server.bat` - Windows startup script
- `server/README.md` - Detailed server documentation
- `src/lib/api.ts` - Frontend API client (replaces TensorFlow.js)

## 🔧 How It Works

1. **Frontend** uploads image → sends to API server
2. **Server** loads model (once, on startup) → processes image → returns prediction
3. **Frontend** displays results

**Benefits:**
- ✅ No browser compilation (model runs on server)
- ✅ No UI freezing
- ✅ Faster predictions (server has more resources)
- ✅ Model only loads once (on server startup)

## ⚠️ Troubleshooting

### "API server is not running"
- Make sure the server is started (see Step 1)
- Check that it's running on `http://localhost:8080`
- Try accessing `http://localhost:8080/health` in your browser

### "Model not found"
- Check that `train/model.keras` exists
- Check that `train/class_mapping.json` exists

### Port 8080 already in use
- Change the port in `server/app.py` (line 95)
- Update `API_URL` in `src/lib/api.ts` to match

### Dependencies not installed
```bash
cd server
python -m pip install -r requirements.txt
```

## 🎯 Next Steps

The server will automatically reload when you make changes (debug mode is enabled). For production, you'd want to:
- Use a production WSGI server (gunicorn, uwsgi)
- Add authentication/rate limiting
- Deploy to a cloud service

But for local development, this setup works perfectly!

