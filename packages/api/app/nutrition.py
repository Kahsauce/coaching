from pydantic import BaseModel

class NutritionPlanRequest(BaseModel):
    body_weight_kg: float
    goal: str = "maintain"  # maintain, gain, lose


class NutritionPlan(BaseModel):
    calories: int
    protein_g: int
    fat_g: int
    carbs_g: int


def calculate_plan(body_weight_kg: float, goal: str = "maintain") -> NutritionPlan:
    if goal == "gain":
        calories = int(body_weight_kg * 35)
    elif goal == "lose":
        calories = int(body_weight_kg * 25)
    else:
        calories = int(body_weight_kg * 30)

    protein = int(body_weight_kg * 1.6)
    fat = int(body_weight_kg * 0.8)
    carbs = int((calories - (protein * 4 + fat * 9)) / 4)

    return NutritionPlan(
        calories=calories,
        protein_g=protein,
        fat_g=fat,
        carbs_g=carbs,
    )
