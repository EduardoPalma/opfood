from typing import List

from dto.dtos import FoodDto


class OptimizerFood:

    def __init__(self, food_universe: List[FoodDto]):
        self.food_universe = food_universe

    def selection(self):
        pass

    def crossover(self):
        pass

    def mutacion(self):
        pass
