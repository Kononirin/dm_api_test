from pydantic import BaseModel
from typing import Optional

class ErrorEnvelope(BaseModel):
    """Модель для ошибок API"""
    status: int
    title: Optional[str] = None
    detail: Optional[str] = None
    code: Optional[str] = None
    timestamp: Optional[str] = None