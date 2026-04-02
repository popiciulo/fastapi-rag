from fastapi import FastAPI
from app.routes.models import router as model_router

app = FastAPI(title="RAG")

@app.get("/")
def root():
    return {"message": "RAG"}

app.include_router(model_router)