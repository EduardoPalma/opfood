from itertools import combinations, product
from typing import List
from api.dto.dtos import FoodDto
from api.dto.enums import NutrientEnum
from api.interface import PopulationStrategy


def optimizer_local(foods: List[FoodDto], target_min: float, target_max: float, max_items: int):
    """
    Optimizador local, toma en cuanta los gramos mas detallados de los alimentos, segun el rango de objetivos a obtener

    :param foods:
    :return:
    """
    best_combination = None
    best_weight = 0
    # Crear combinaciones de alimentos limitadas por `max_items`
    food_combinations = combinations(foods, min(len(foods), max_items))

    for combo in food_combinations:
        # Generar todas las combinaciones de porciones para los alimentos seleccionados
        unit_combos = list(
            product(*[
                [
                    (food["name"], unit, portions * weight)
                    for unit, weight in food["units"].items()
                    for portions in range(1, food["max_portions"] + 1)
                ]
                for food in combo
            ])
        )

        for unit_combo in unit_combos:
            total_weight = sum(item[2] for item in unit_combo)
            if total_weight <= target_max and total_weight > target_min:
                best_combination = unit_combo
                best_weight = total_weight

            # Si encontramos la solución exacta, detenernos
            if best_weight <= target_max:
                return best_combination, best_weight

    return best_combination, best_weight


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
