from ollama import Client, ListResponse, AsyncClient, list, chat 
from fastapi import APIRouter, HTTPException
from app.services.ai_service import list_models, create_new_model, get_streaming_model_answer, get_model_answer
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.schemas.ai_schemas import ModelParameters, CreateModel

router = APIRouter(tags=["AI Models"], prefix="/ai")

@router.post("/ask")
async def ask_model(parameters: ModelParameters):
    if parameters.streamed:
        return StreamingResponse(get_streaming_model_answer(parameters), media_type="text/event-stream", headers={"Cache-Control": "no-cache"})
    else:
        return await get_model_answer(parameters)  

@router.get("/models")
async def get_models(family: str | None = None):
    return await list_models(family)
    
@router.post("/create_model")
async def create_model(model: CreateModel):
    return await create_new_model(model)