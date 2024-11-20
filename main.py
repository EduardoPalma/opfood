from contextlib import asynccontextmanager
from typing import List
from api.init_app import init_run
from api.dto.dtos import FoodDto
from fastapi import FastAPI

data_food: List[FoodDto] = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    global data_food
    await init_run(data_food)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/food/meal_plan")
async def get_food_meal_plan():
    return {"error": "Food not found"}


@app.get("/recipe/meal_plan")
async def get_recipe_meal_plan():
    print(len(data_food))
    return {"hi": "hola"}
