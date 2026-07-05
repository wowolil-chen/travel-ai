from fastapi import FastAPI

app = FastAPI(
    title="Travel AI",
    version="1.0.0",
    description="旅游规划智能体"
)


@app.get("/")
async def root():
    return {
        "message": "Travel AI Backend"
    }


@app.get("/health")
async def health():
    return {
        "status": "ok"
    }