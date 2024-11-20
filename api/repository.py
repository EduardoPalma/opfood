from typing import List

from api.dto.dtos import FoodDto, FoodPortions, NutrientFood
from api.interface import IFoodRepository
from db_mongo.models_mongo import Food



class FoodRepository(IFoodRepository):

    async def all_food(self) -> List[FoodDto]:
        foods = await Food.find_all().to_list()

        # resolver relation in document
        for food in foods:
            await food.fetch_link(Food.nutrients)

        result: List[FoodDto] = []
        # data transfert object
        for food in foods:
            result.append(FoodDto(name=food.name, category=food.foodCategory,
                                  foodPortions=[FoodPortions(name=portion.name, abbreviation=portion.abbreviation,
                                                             grams=portion.grams, amount=portion.amount)
                                                for portion in food.foodPortions],
                                  nutrients=[
                                      NutrientFood(name=nutrient.name, unit=nutrient.unit, amount=nutrient.amount)
                                      for nutrient in food.nutrients]))

        return result
