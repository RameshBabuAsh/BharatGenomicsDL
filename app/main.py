from fastapi import FastAPI
from app.api.version1.endpoints import ESM2ForPTMs

app = FastAPI()

app.include_router(ESM2ForPTMs.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
