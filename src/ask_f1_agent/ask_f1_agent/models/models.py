import time

from typing import List

from pydantic import BaseModel


class ModelCard(BaseModel):
    id: str
    object: str = "model"
    created: int = int(time.time())
    owned_by: str


class ModelList(BaseModel):
    object: str = "list"
    data: List[ModelCard]
