from typing import List
from api.dto.dtos import FoodDto
from api.dto.enums import NutrientEnum
from api.interface import PopulationStrategy


def optimizer_local(foods: List[FoodDto], target_min: float, target_max: float) -> List[int]:
    """
    Optimizador local, toma en cuanta los gramos mas detallados de los alimentos, segun el rango de objetivos a obtener

    :param foods:
    :return:
    """
    pass


class PopulationDefault(PopulationStrategy):
    def generated_population(self, universe_food: List[FoodDto],
                             target_nutrient: List[NutrientEnum],
                             target_fitness: List[float]):
        # seleccionar solo los food con los target de los NutrientEnum
        # generar para cada unas de las categorias del plato del buen comer
        # estructurar todo a las clases definidas
        # definir una forma de seleccionar una cantidad ya sean los gramos para este alimento
        # funcion que calcule los targe
        pass
