from fastapi import FastAPI
import chromadb
from fastapi.middleware.cors import CORSMiddleware
from app.routes.ai_router import router as ai_model_router

origins = [
    "http://localhost:5173",
]

app = FastAPI(title="RAG")

@app.on_event("startup")
async def startup():
    app.state.chroma_client = await chromadb.AsyncHttpClient(
        host="localhost",
        port=5131
    )

    app.state.collection = await app.state.chroma_client.get_or_create_collection(
        name="journal"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "RAG"}

app.include_router(ai_model_router)