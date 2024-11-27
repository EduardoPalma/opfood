from typing import Mapping, Any, List
from pymongo import MongoClient
from pathlib import Path
import json
from pymongo.synchronous.database import Database
from script.translate import Translate


def read_json_food_data_central(path_file: str):
    try:
        with open(path_file, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
        return datos
    except FileNotFoundError:
        print(f"Error: El archivo {path_file} no se encontró.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error al decodificar el archivo JSON: {e}")
        return None


def translate_bulk(texts: List[str]) -> List[str]:
    texts = Translate.translate_google(texts, "es", "en")
    return texts


def translate_single(texts: str) -> str:
    texts = Translate.translate_google_single(texts, "es", "en")
    return texts


def convert_food_portions(food_portions):
    data_dict_portions = [{"name": translate_single(portions.get("modifier")),
                           "abbreviation": translate_single(portions.get("measureUnit").get("abbreviation")),
                           "grams": float(portions.get("gramWeight")),
                           "amount": float(portions.get("amount") if portions.get("amount") is not None else 1.0)} for
                          portions in food_portions]
    print(data_dict_portions)
    return data_dict_portions


def transform_data_in_document(data_json, db_instance: Database[Mapping[str, Any]]):
    # create collection if not exist
    db_collection_nutrient = db_instance["nutrient_food"]
    db_collection_food = db_instance["food"]

    for food_information in data_json['SRLegacyFoods']:
        name = translate_single(food_information.get("description"))
        food_portions = convert_food_portions(food_information.get("foodPortions"))
        food_category = translate_single(food_information.get("foodCategory").get("description"))

        collections_nutrient = []
        for nutrients in food_information["foodNutrients"]:
            name_nutrient = translate_single(nutrients["nutrient"]["name"])
            unit = nutrients["nutrient"]["unitName"]
            amount = nutrients.get("amount")
            data_nutrient = {"name": name_nutrient, "unit": unit, "amount": amount}
            collections_nutrient.append(data_nutrient)

        result = db_collection_nutrient.insert_many(collections_nutrient)
        if result:
            ids = [_id for _id in result.inserted_ids]
            data_food = {"name": name, "foodCategory": food_category, "foodPortions": food_portions, "nutrients": ids}
            db_collection_food.insert_one(data_food)


# collection
# food
# nutrient
if __name__ == '__main__':
    client = MongoClient("mongodb://localhost:27017/")
    db = client["foods_legacy"]

    path = Path(__file__).resolve().parent.parent
    data = read_json_food_data_central(path / "files_utils/FoodData_Central_sr_legacy_food_json_2021-10-28.json") # 4455
    transform_data_in_document(data, db)
