from pydantic import BaseModel

class ModelParameters(BaseModel):
    model_name: str = "gemma3:1b"
    prompt: str = "What is fastAPI?"
    streamed: bool = False
    
class CreateModel(BaseModel):
    selected_model: str
    new_model_name: str | None = None
    system_prompt: str