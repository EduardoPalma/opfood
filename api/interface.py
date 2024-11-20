from abc import ABC, abstractmethod
from typing import List

from api.dto.dtos import FoodDto
from api.dto.enums import NutrientEnum


class IFoodRepository(ABC):
    @abstractmethod
    async def all_food(self) -> List[FoodDto]:
        pass


class SelectionStrategy(ABC):
    @abstractmethod
    def select(self, population):
        pass


class CrossoverStrategy(ABC):
    @abstractmethod
    def crossover(self, parent1, parent2):
        pass


class MutationStrategy(ABC):
    @abstractmethod
    def mutate(self, individual):
        pass


class PopulationStrategy(ABC):
    @abstractmethod
    def generated_population(self, universe_food: List[FoodDto],
                             target: List[NutrientEnum],
                             target_fitness: List[float]):
        pass
