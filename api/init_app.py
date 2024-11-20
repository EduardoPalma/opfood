from typing import List
from api.dto.dtos import FoodDto
from api.repository import FoodRepository
from db_mongo.models_mongo import Food, NutrientFood
from db_mongo.mongodb import MongoClient


async def init_run(data_food: List[FoodDto]):
    client_mongo = MongoClient()
    await client_mongo.init_models([Food, NutrientFood])
    food_repository = FoodRepository()
    data_food.extend(await food_repository.all_food())