from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI
from db_mongo.models_mongo import Food, NutrientFood # no deberia estar
from db_mongo.mongodb import MongoClient
from db_mongo.repository import FoodRepository # archivo llamado API
from dto.dtos import FoodDto

data_food: List[FoodDto] = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    client_mongo = MongoClient()
    await client_mongo.init_models([Food, NutrientFood])

    global data_food
    data_food.extend(await food_repository.all_food())
    yield


app = FastAPI(lifespan=lifespan)
food_repository = FoodRepository()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/food/meal_plan")
async def get_food_meal_plan():
    food_item = await Food.get(id)
    await food_item.fetch_link(Food.nutrients)
    if food_item:
        return food_item  # Retorna el documento convertido a diccionario
    else:
        return {"error": "Food not found"}


@app.get("/recipe/meal_plan")
async def get_recipe_meal_plan():
    print(len(data_food))
    return {"hi" : "hola"}
