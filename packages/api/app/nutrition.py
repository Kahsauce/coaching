from pydantic import BaseModel

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
