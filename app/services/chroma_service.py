from ollama import embed
import uuid
from datetime import datetime, timezone, timedelta
from app.schemas.chroma_schemas import AddJournalEntry

collection_name = "journal"

embedding_model = "qwen3-embedding:0.6b"

class OllamaEmbedding:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def __call__(self, input: list[str]) -> list[list[float]]:
        # ChromaDB așteaptă un return list[list[float]]
        return [embed(model=self.model_name, text=text) for text in input]

    def name(self) -> str:
        return f"ollama-{self.model_name}"


async def create_collection_entry(client, journal_entry: AddJournalEntry, ):
    collection = await client.get_collection(name=collection_name)

    await collection.add(
        documents=journal_entry.documents,
        ids=[str(uuid.uuid4()) for _ in journal_entry.documents],
        metadatas=[
            {"user_id": 1, "timestamp": datetime.now(timezone.utc).isoformat()} 
            for _ in journal_entry.documents
            ]
        )
    
    return collection


async def get_collection_entry(client, query: str):
    collection = await client.get_collection(name=collection_name)
    query_result = await collection.query(
        query_texts=[query],
        n_results=5,
        where={"user_id": 1},
    )
    print(query_result)
    return query_result