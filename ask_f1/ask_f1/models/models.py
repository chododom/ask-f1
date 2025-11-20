from pydantic import BaseModel
from typing import List
import time


class ModelCard(BaseModel):
    id: str
    object: str = "model"
    created: int = int(time.time())
    owned_by: str


class ModelList(BaseModel):
    object: str = "list"
    data: List[ModelCard]
