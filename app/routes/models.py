from ollama import Client, ListResponse, list
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter(tags=["AI Models"])


class CreateModel(BaseModel):
    selected_model: str
    new_model_name: str | None = None
    system_prompt: str

@router.get("/models")
async def list_models(family: str | None = None):
    response: ListResponse = list()
    if not response.models:
        raise HTTPException(status_code=404, detail="No models found")
    
    families: set[str] = {entry.details.family for entry in response.models}

    if family:
        filtered = [m for m in response.models if m.details.family == family]
        return {"families": families, "models": filtered}

    return {"families": families, "models": response.models}
    
@router.post("/create_model")
async def create_new_model(model: CreateModel):
    model.new_model_name = model.new_model_name or f"{model.selected_model}-assistant"
    model.system_prompt = model.system_prompt or f"You are my personal assistant"

    if model_exists(model.new_model_name):
        return {"message":"model name already exists"}
    
    client = Client()
    response = client.create(
      model=model.new_model_name,
      from_=model.selected_model,
      system=model.system_prompt,
      stream=False,
    )

    return response.status


def model_exists(name: str):    
    response: ListResponse = list()    
    return any(f.model == name for f in response.models)