from datetime import datetime, date
from typing import Optional, List
import re
from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict



class SNote(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str = Field(..., min_length=1, max_length=150, description="Имя заметки, от 1 до 150 символов")
    content: Optional[str] = Field(None, description="Содержимое, не более 1000 символов")
    tags: Optional[List[str]] = Field([], description="Теги заметки")

class SNoteAdd(BaseModel):
    title: str = Field(..., min_length=1, max_length=150, description="Имя заметки, от 1 до 150 символов")
    content: Optional[str] = Field(None, description="Содержимое, не более 1000 символов")
    tags: Optional[List[str]] = Field([], description="Теги заметки")