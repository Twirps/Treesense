# Tree Classification API Server

This server runs the Keras model on the backend, avoiding browser compilation issues.

## Setup

1. **Install dependencies:**
   
   **Option 1: Use the startup script (Windows)**
   ```bash
   cd server
   start_server.bat
   ```
   
   **Option 2: Manual installation**
   ```bash
   cd server
   # Use Python 3.12
   python -m pip install -r requirements.txt
   # Or if python is in PATH:
   pip install -r requirements.txt
   ```

2. **Verify files exist:**
   - `../train/model.keras` - The trained model (should exist)
   - `../train/class_mapping.json` - Class name mapping (should exist)

## Running the Server

**Windows PowerShell (recommended):**
```powershell
cd server
.\start_server.ps1
```

**Windows CMD or PowerShell (batch file):**
```powershell
cd server
.\start_server.bat
```

**Manual (if batch file doesn't work):**
```bash
cd server
python app.py
# Or with full path:
%LOCALAPPDATA%\Programs\Python\Python312\python.exe app.py
```

The server will:
- Load the model on startup
- Listen on `http://localhost:8080`
- Accept POST requests at `/predict`

## API Endpoints

### Health Check
```
GET http://localhost:8080/health
```

### Prediction
```
POST http://localhost:8080/predict
Content-Type: multipart/form-data
Body: image file
```

Response:
```json
{
  "className": "Red_Maple",
  "confidence": 0.95,
  "top3": [
    {"className": "Red_Maple", "confidence": 0.95},
    {"className": "White_Oak", "confidence": 0.03},
    {"className": "Tulip_Poplar", "confidence": 0.02}
  ],
  "allProbabilities": [...]
}
```

## Frontend Integration

The frontend automatically uses this API when available. Make sure:
1. Server is running on `http://localhost:8080`
2. Frontend is running (usually `http://localhost:5173` or similar)
3. CORS is enabled (already configured in `app.py`)

## Troubleshooting

- **"API server is not running"**: Start the server with `python app.py`
- **Model not found**: Check that `model.keras` exists in `../train/`
- **Port already in use**: Change port in `app.py` (line 128) or kill the process using port 8080

