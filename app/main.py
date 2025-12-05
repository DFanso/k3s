from fastapi import FastAPI
from datetime import datetime
import os

app = FastAPI(title="K3s Demo App")

@app.get("/")
def root():
    return {
        "message": "Hello from K3s! 🚀",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "timestamp": datetime.now().isoformat(),
        "hostname": os.getenv("HOSTNAME", "unknown")
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

