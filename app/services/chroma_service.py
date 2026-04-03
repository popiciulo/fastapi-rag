import chromadb
import uuid
from datetime import datetime, timezone
from app.schemas.chroma_schemas import AddJournalEntry

collection_name = "journal"

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


async def get_collection(client):
    collection = await client.get_collection(name=collection_name)