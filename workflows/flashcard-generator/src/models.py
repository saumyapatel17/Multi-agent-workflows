from pydantic import BaseModel
from typing import List

# Data Models
class QACard(BaseModel):
    question: str
    answer: str
    extra: str

class Flashcard_model(BaseModel):
    cards: List[QACard]