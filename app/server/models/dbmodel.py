from typing import Optional, Any

from pydantic import BaseModel, Schema, validator


class IDModel(BaseModel):
    id: Optional[Any] = Schema(..., alias="_id")

    @validator("id")
    def validate_id(cls, id):
        return str(id)
