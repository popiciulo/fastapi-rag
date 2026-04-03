from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class Metadata(BaseModel):
    user_id: int
    timestamp: str

    model_config = ConfigDict(extra="forbid")

    def to_dict(self) -> dict:
        """
        Returnează doar valorile definite (exclude None).
        """
        return self.model_dump(exclude_none=True)    

class GetJournalEntry(BaseModel):
    ids: list[str]
    documents: list[str]
    metadata: Metadata = Field(default_factory=Metadata)

    model_config = ConfigDict(extra="forbid")

class AddJournalEntry(BaseModel):
    documents: list[str]

    model_config = ConfigDict(extra="forbid")
