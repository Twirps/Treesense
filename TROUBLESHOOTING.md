# Troubleshooting Guide

## API Server Connection Issues

### Error: `ERR_BLOCKED_BY_CLIENT` or `Failed to fetch`

**Note:** The server now uses port **8080** to avoid ad blocker issues.

If you still see this error:

1. **Disable ad blocker for localhost:**
   - Open your ad blocker settings
   - Add `localhost` or `127.0.0.1` to the whitelist/allowlist
   - Refresh the page

2. **Use a different port:**
   - Edit `server/app.py` line 128: change `port=8080` to another port (e.g., `port=8000`)
   - Edit `src/lib/api.ts` line 14: change `'http://localhost:8080'` to match
   - Restart both server and frontend

3. **Try a different browser:**
   - Some browsers/extensions are more aggressive
   - Try Chrome, Firefox, or Edge

### Error: "API server is not running"

**Check if server is running:**
```powershell
# Check if port 8080 is in use
netstat -ano | findstr :8080
```

**Start the server:**
```powershell
cd server
.\start_server.ps1
```

You should see:
```
✅ Server ready! Listening on http://localhost:8080
```

### Error: "Cannot connect to API server"

**Checklist:**
1. ✅ Server is running (see above)
2. ✅ Server shows "Server ready!" message
3. ✅ No firewall blocking port 8080
4. ✅ Ad blocker disabled for localhost
5. ✅ Frontend and server are on same machine

**Test the server directly:**
Open in browser: `http://localhost:8080/health`

Should return: `{"status":"ok","message":"Tree Classification API is running"}`

### Server won't start

**"Python not found":**
- Make sure Python 3.12 is installed
- Update path in `start_server.ps1` or `start_server.bat`

**"Module not found":**
```powershell
cd server
python -m pip install -r requirements.txt
```

**"Model not found":**
- Check that `train/model.keras` exists
- Check that `train/class_mapping.json` exists

### Still having issues?

1. Check server console for error messages
2. Check browser console (F12) for detailed errors
3. Make sure both server and frontend are running
4. Try restarting both

