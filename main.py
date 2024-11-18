

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Ingredient, NutritionalValue, IngredientMeasure

# Conexión a la base de datos
DATABASE_URL = "postgresql://nutrifoods_dev:MVmYneLqe91$@ep-still-truth-a4eitqn3.us-east-1.aws.neon.tech/NutrifoodsDB?sslmode=require"
engine = create_engine(DATABASE_URL)

# Crear la sesión
Session = sessionmaker(bind=engine)
session = Session()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    foods = session.query(Ingredient, IngredientMeasure).join(IngredientMeasure).limit(6).all()
    for ingredient, measure in foods:
        print(ingredient.name, measure.name)
