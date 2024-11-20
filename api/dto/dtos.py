from typing import List

from pydantic import BaseModel


class NutrientFood(BaseModel):
    name: str
    unit: str
    amount: float | None


class FoodPortions(BaseModel):
    name: str
    abbreviation: str
    grams: float
    amount: float


class FoodDto(BaseModel):
    name: str
    category: str
    foodPortions: List[FoodPortions]
    nutrients: List[NutrientFood]
