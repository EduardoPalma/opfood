from abc import ABC, abstractmethod
from typing import List
from dto.dtos import FoodDto


class IFoodRepository(ABC):
    @abstractmethod
    async def all_food(self) -> List[FoodDto]:
        pass