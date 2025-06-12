from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClientCommentBase(BaseModel):
    client_id: int
    comment_text: str

class ClientCommentCreate(ClientCommentBase):
    created_by: Optional[str] = "system"  # preparado para login real después

class ClientCommentResponse(ClientCommentBase):
    id: int
    created_by: str
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 equivalente de orm_mode
