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


class NutritionEntry(BaseModel):
    """Log de nutrition et d'hydratation pour une journée."""

    id: int
    date: date
    calories: int = Field(0, ge=0)
    hydration_l: float = Field(0.0, ge=0.0)
    carbs_g: int = Field(0, ge=0)
    protein_g: int = Field(0, ge=0)
    fat_g: int = Field(0, ge=0)


class Injury(BaseModel):
    """Période de blessure nécessitant une adaptation des entraînements."""

    id: int
    start_date: date
    end_date: Optional[date] = None
    description: str = ""
