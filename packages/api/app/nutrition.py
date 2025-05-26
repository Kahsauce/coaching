from datetime import date, timedelta
from typing import List

from pydantic import BaseModel
from .models import NutritionEntry

class NutritionPlanRequest(BaseModel):
    body_weight_kg: float
    goal: str = "maintain"  # maintain, gain, lose


class NutritionPlan(BaseModel):
    calories: int
    protein_g: int
    fat_g: int
    carbs_g: int
    hydration_l: float


def calculate_plan(body_weight_kg: float, goal: str = "maintain") -> NutritionPlan:
    if goal == "gain":
        calories = int(body_weight_kg * 35)
        protein = int(body_weight_kg * 1.8)
    elif goal == "lose":
        calories = int(body_weight_kg * 25)
        protein = int(body_weight_kg * 2.0)
    else:
        calories = int(body_weight_kg * 30)
        protein = int(body_weight_kg * 1.6)
    fat = int(body_weight_kg * 0.8)
    carbs = int((calories - (protein * 4 + fat * 9)) / 4)
    hydration_l = round(body_weight_kg * 0.035, 1)

    return NutritionPlan(
        calories=calories,
        protein_g=protein,
        fat_g=fat,
        carbs_g=carbs,
        hydration_l=hydration_l,
    )


def average_hydration(
    entries: List[NutritionEntry], days: int = 7, today: date | None = None
) -> float:
    """Retourne l'hydratation moyenne (en litres) sur les *days* derniers jours."""
    if today is None:
        today = date.today()
    start = today - timedelta(days=days - 1)
    values = [e.hydration_l for e in entries if start <= e.date <= today]
    if not values:
        return 0.0
    return round(sum(values) / len(values), 2)
