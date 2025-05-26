from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional

class TrainingSession(BaseModel):
    id: int
    date: date
    sport: str
    description: str = ""
    duration_min: int = 0
    rpe: Optional[int] = None
    completed: bool = False
