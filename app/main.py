import chromadb
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.ai_router import router as ai_model_router
from app.services.chroma_service import OllamaEmbedding

origins = [
    "http://localhost:5173",
]

ollama_embedding_fn = OllamaEmbedding("qwen3-embedding:0.6b")

app = FastAPI(title="RAG")

@app.on_event("startup")
async def startup():
    app.state.chroma_client = await chromadb.AsyncHttpClient(
        host="localhost",
        port=5131,
        settings=chromadb.Settings(
            chroma_api_impl="rest",
            chroma_server_host="localhost",
            chroma_server_http_port=5131,
        )
    )
    
    app.state.collection = await app.state.chroma_client.get_or_create_collection(
        name="journal",
        embedding_function=ollama_embedding_fn
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