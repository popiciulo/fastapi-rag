from fastapi import FastAPI
from app.routes.ai_router import router as ai_model_router

app = FastAPI(title="RAG")

@app.get("/")
def root():
    return {"message": "RAG"}

app.include_router(ai_model_router)