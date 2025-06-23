from pydantic import BaseModel, validator
from typing import Any

class Record(BaseModel):
    categoria: str
    valor: float

    @validator("valor", pre=True)
    def to_float(cls, v: Any):
        return float(v) if v not in (None, "", "NaN") else None
