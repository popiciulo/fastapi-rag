from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse

from app.schemas.chroma_schemas import AddJournalEntry
from app.schemas.ai_schemas import ModelParameters, CreateModel
from app.services import ai_service
from app.services import chroma_service


router = APIRouter(tags=["AI Models"], prefix="/ai")

def get_chroma_client(request: Request):
    return request.app.state.chroma_client

@router.post("/ask")
async def ask_model(parameters: ModelParameters):
    if parameters.streamed:
        return StreamingResponse(ai_service.get_streaming_model_answer(parameters), media_type="text/event-stream", headers={"Cache-Control": "no-cache"})
    else:
        return await ai_service.get_model_answer(parameters)  
    
@router.post("/personal/ask")
async def ask_personal_model(query: str, chroma_client = Depends((get_chroma_client))):
    return await ai_service.get_personal_model_answer(query, chroma_client)

@router.post("/personal/tell")
async def tell_personal_model(journal_entry: AddJournalEntry, chroma_client = Depends((get_chroma_client))):
    await chroma_service.create_collection_entry(chroma_client, journal_entry)

@router.get("/models")
async def get_models(family: str | None = None):
    return await ai_service.list_models(family)
    
@router.post("/create_model")
async def create_model(model: CreateModel):
    return await ai_service.create_new_model(model)