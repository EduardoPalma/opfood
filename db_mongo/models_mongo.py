from typing import List
from beanie import Document, Link
from pydantic import BaseModel


class NutrientFood(Document):
    name: str
    unit: str
    amount: float | None

    class Settings:
        name = "nutrient_food"


class FoodPortions(BaseModel):
    name: str
    abbreviation: str
    grams: float
    amount: float


class Food(Document):
    name: str
    foodCategory: str
    foodPortions: List[FoodPortions]
    nutrients: List[Link[NutrientFood]]

    class Settings:
        name = "food"
