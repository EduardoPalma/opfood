from typing import List
from api.dto.dtos import FoodDto
from api.dto.enums import FoodCategory
from api.interface import SelectionStrategy, CrossoverStrategy, MutationStrategy, PopulationStrategy


class Food:
    def __init__(self, category: FoodCategory, amount: float, grams: float, unit: str,
                 nutrients: List[float]):
        self.category = category
        self.amount = amount
        self.grams = grams
        self.unit = unit
        self.nutrients: List[float] = nutrients


class Chromosome:
    def __init__(self, ):
        self.foods: List[Food] = []
        self.fitness: float = 0.0


class OptimizerFood:

    def __init__(self,
                 food_universe: List[FoodDto],
                 method_population: PopulationStrategy,
                 method_selection: SelectionStrategy,
                 method_crossover: CrossoverStrategy,
                 method_mutation: MutationStrategy):
        self.food_universe = food_universe
        self.method_population = method_population
        self.method_selection = method_selection
        self.method_crossover = method_crossover
        self.method_mutation = method_mutation
        self.population: List[Chromosome] = []

    def generated_food_meal_plan(self):
        pass

    def _generated_population(self):
        pass

    def _selection(self):
        pass

    def _crossover(self):
        pass

    def _mutacion(self):
        pass
