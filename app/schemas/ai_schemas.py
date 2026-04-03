from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ChatOptions(BaseModel):
    temperature: Optional[float] = Field(default=0.2, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=1024, gt=0)
    top_p: Optional[float] = Field(default=0.9, ge=0, le=1)
    top_k: Optional[int] = Field(default=50, ge=0)
    top_n: Optional[int] = Field(default=1, ge=1)
    frequency_penalty: Optional[float] = Field(default=0, ge=0)
    presence_penalty: Optional[float] = Field(default=0, ge=0)

    model_config = ConfigDict(extra="forbid")

    def to_dict(self) -> dict:
        """
        Returnează doar valorile definite (exclude None).
        Compatibil direct cu client.chat(options=...)
        """
        return self.model_dump(exclude_none=True)    

class ModelParameters(BaseModel):
    model_name: str = "gemma4:e2b"
    prompt: str
    streamed: bool = False
    history: bool = False
    options: ChatOptions = Field(default_factory=ChatOptions)

    model_config = ConfigDict(extra="forbid")


class CreateModel(BaseModel):
    selected_model: str
    new_model_name: str | None = None
    system_prompt: str