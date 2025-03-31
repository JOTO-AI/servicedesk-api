from fastapi import FastAPI
import sys
sys.path.append("..")
from app.api.endpoints import router

app = FastAPI(title="Service Desk API")
app.include_router(router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 