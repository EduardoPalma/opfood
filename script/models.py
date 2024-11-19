# coding: utf-8
from sqlalchemy import ARRAY, Boolean, Column, Date, DateTime, Float, ForeignKey, Index, Integer, String, Table, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class DailyPlan(Base):
    __tablename__ = 'daily_plan'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('nutrifoods.daily_plan_id_seq'::regclass)"))
    days = Column(ARRAY(Integer()), nullable=False, server_default=text("ARRAY[]::integer[]"))
    physical_activity_level = Column(Integer, nullable=False)
    physical_activity_factor = Column(Float(53), nullable=False)
    adjustment_factor = Column(Float(53), nullable=False)

    nutritional_targets = relationship('NutritionalTarget', secondary='nutrifoods.daily_plan_nutritional_target')
    nutritional_values = relationship('NutritionalValue', secondary='nutrifoods.daily_plan_nutritional_value')


class Ingredient(Base):
    __tablename__ = 'ingredient'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('nutrifoods.ingredient_id_seq'::regclass)"))
    name = Column(String(64), nullable=False, unique=True)
    synonyms = Column(ARRAY(String(length=64)), nullable=False, server_default=text("ARRAY[]::character varying[]"))
    is_animal = Column(Boolean, nullable=False)
    food_group = Column(Integer, nullable=False)

    nutritional_values = relationship('NutritionalValue', secondary='nutrifoods.ingredient_nutrient')


class NutritionalTarget(Base):
    __tablename__ = 'nutritional_target'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('nutrifoods.nutritional_target_id_seq'::regclass)"))
    nutrient = Column(Integer, nullable=False)
    expected_quantity = Column(Float(53), nullable=False)
    actual_quantity = Column(Float(53))
    expected_error = Column(Float(53), nullable=False)
    actual_error = Column(Float(53))
    unit = Column(Integer, nullable=False)
    threshold_type = Column(Integer, nullable=False)
    is_priority = Column(Boolean, nullable=False)


class NutritionalValue(Base):
    __tablename__ = 'nutritional_value'
    __table_args__ = (
        Index('nutritional_value_idx', 'nutrient', 'quantity'),
        {'schema': 'nutrifoods'}
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('nutrifoods.nutritional_value_id_seq'::regclass)"))
    nutrient = Column(Integer, nullable=False)
    quantity = Column(Float(53), nullable=False)
    unit = Column(Integer, nullable=False)
    daily_value = Column(Float(53))

    recipes = relationship('Recipe', secondary='nutrifoods.recipe_nutrient')


class Nutritionist(Base):
    __tablename__ = 'nutritionist'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(UUID, primary_key=True, server_default=text("nutrifoods.uuid_generate_v4()"))
    username = Column(String(50), nullable=False, unique=True)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    joined_on = Column(DateTime(True), nullable=False, server_default=text("(now())::timestamp without time zone"))


class Recipe(Base):
    __tablename__ = 'recipe'
    __table_args__ = (
        UniqueConstraint('name', 'author'),
        {'schema': 'nutrifoods'}
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('nutrifoods.recipe_id_seq'::regclass)"))
    name = Column(Text, nullable=False)
    author = Column(String(64), nullable=False)
    url = Column(Text, nullable=False, unique=True)
    portions = Column(Integer)
    time = Column(Integer)
    difficulty = Column(Integer)
    meal_types = Column(ARRAY(Integer()), nullable=False, server_default=text("ARRAY[]::integer[]"))
    dish_types = Column(ARRAY(Integer()), nullable=False, server_default=text("ARRAY[]::integer[]"))


class DailyMenu(Base):
    __tablename__ = 'daily_menu'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('nutrifoods.daily_menu_id_seq'::regclass)"))
    daily_plan_id = Column(ForeignKey('nutrifoods.daily_plan.id'), nullable=False)
    intake_percentage = Column(Float(53), nullable=False)
    meal_type = Column(Integer, nullable=False)
    hour = Column(String(8), nullable=False)

    daily_plan = relationship('DailyPlan')
    nutritional_targets = relationship('NutritionalTarget', secondary='nutrifoods.daily_menu_nutritional_target')
    nutritional_values = relationship('NutritionalValue', secondary='nutrifoods.daily_menu_nutritional_value')


t_daily_plan_nutritional_target = Table(
    'daily_plan_nutritional_target', metadata,
    Column('daily_plan_id', ForeignKey('nutrifoods.daily_plan.id'), primary_key=True, nullable=False),
    Column('nutritional_target_id', ForeignKey('nutrifoods.nutritional_target.id'), primary_key=True, nullable=False),
    schema='nutrifoods'
)


t_daily_plan_nutritional_value = Table(
    'daily_plan_nutritional_value', metadata,
    Column('daily_plan_id', ForeignKey('nutrifoods.daily_plan.id'), primary_key=True, nullable=False),
    Column('nutritional_value_id', ForeignKey('nutrifoods.nutritional_value.id'), primary_key=True, nullable=False),
    schema='nutrifoods'
)


class IngredientMeasure(Base):
    __tablename__ = 'ingredient_measure'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('nutrifoods.ingredient_measure_id_seq'::regclass)"))
    name = Column(String(64), nullable=False)
    grams = Column(Float(53), nullable=False)
    is_default = Column(Boolean, nullable=False)
    ingredient_id = Column(ForeignKey('nutrifoods.ingredient.id'), nullable=False)

    ingredient = relationship('Ingredient')


t_ingredient_nutrient = Table(
    'ingredient_nutrient', metadata,
    Column('ingredient_id', ForeignKey('nutrifoods.ingredient.id'), primary_key=True, nullable=False),
    Column('nutritional_value_id', ForeignKey('nutrifoods.nutritional_value.id'), primary_key=True, nullable=False),
    schema='nutrifoods'
)


class Patient(Base):
    __tablename__ = 'patient'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(UUID, primary_key=True, server_default=text("nutrifoods.uuid_generate_v4()"))
    joined_on = Column(DateTime(True), nullable=False, server_default=text("(now())::timestamp without time zone"))
    nutritionist_id = Column(ForeignKey('nutrifoods.nutritionist.id'), nullable=False)

    nutritionist = relationship('Nutritionist')


class Addres(Patient):
    __tablename__ = 'address'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(ForeignKey('nutrifoods.patient.id'), primary_key=True)
    street = Column(Text, nullable=False)
    number = Column(Integer, nullable=False)
    postal_code = Column(Integer)
    province = Column(Integer, nullable=False)


class ContactInfo(Patient):
    __tablename__ = 'contact_info'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(ForeignKey('nutrifoods.patient.id'), primary_key=True)
    mobile_phone = Column(String(16), nullable=False)
    fixed_phone = Column(String(16))
    email = Column(Text, nullable=False, unique=True)


class PersonalInfo(Patient):
    __tablename__ = 'personal_info'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(ForeignKey('nutrifoods.patient.id'), primary_key=True)
    rut = Column(String(16), nullable=False, unique=True)
    names = Column(String(50), nullable=False)
    last_names = Column(String(50), nullable=False)
    biological_sex = Column(Integer, nullable=False)
    birthdate = Column(Date, nullable=False)


t_recipe_nutrient = Table(
    'recipe_nutrient', metadata,
    Column('recipe_id', ForeignKey('nutrifoods.recipe.id'), primary_key=True, nullable=False),
    Column('nutritional_value_id', ForeignKey('nutrifoods.nutritional_value.id'), primary_key=True, nullable=False),
    schema='nutrifoods'
)


class RecipeQuantity(Base):
    __tablename__ = 'recipe_quantity'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('nutrifoods.recipe_quantity_id_seq'::regclass)"))
    recipe_id = Column(ForeignKey('nutrifoods.recipe.id'), nullable=False)
    ingredient_id = Column(ForeignKey('nutrifoods.ingredient.id'), nullable=False)
    grams = Column(Float(53), nullable=False)

    ingredient = relationship('Ingredient')
    recipe = relationship('Recipe')


class RecipeStep(Base):
    __tablename__ = 'recipe_step'
    __table_args__ = (
        UniqueConstraint('recipe_id', 'number'),
        {'schema': 'nutrifoods'}
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('nutrifoods.recipe_step_id_seq'::regclass)"))
    recipe_id = Column(ForeignKey('nutrifoods.recipe.id'), nullable=False)
    number = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)

    recipe = relationship('Recipe')


class Consultation(Base):
    __tablename__ = 'consultation'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(UUID, primary_key=True, server_default=text("nutrifoods.uuid_generate_v4()"))
    type = Column(Integer, nullable=False)
    purpose = Column(Integer, nullable=False)
    registered_on = Column(Date, server_default=text("((now())::timestamp without time zone)::date"))
    patient_id = Column(ForeignKey('nutrifoods.patient.id'), nullable=False)

    patient = relationship('Patient')
    daily_plans = relationship('DailyPlan', secondary='nutrifoods.meal_plan')


class Anthropometry(Consultation):
    __tablename__ = 'anthropometry'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(ForeignKey('nutrifoods.consultation.id'), primary_key=True)
    height = Column(Integer, nullable=False)
    weight = Column(Float(53), nullable=False)
    bmi = Column(Float(53), nullable=False)
    muscle_mass_percentage = Column(Float(53), nullable=False)
    waist_circumference = Column(Float(53), nullable=False)
    created_on = Column(DateTime(True), server_default=text("(now())::timestamp without time zone"))
    last_updated = Column(DateTime(True), server_default=text("(now())::timestamp without time zone"))


class ClinicalAnamnesi(Consultation):
    __tablename__ = 'clinical_anamnesis'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(ForeignKey('nutrifoods.consultation.id'), primary_key=True)
    created_on = Column(DateTime(True), server_default=text("(now())::timestamp without time zone"))
    last_updated = Column(DateTime(True), server_default=text("(now())::timestamp without time zone"))


class NutritionalAnamnesi(Consultation):
    __tablename__ = 'nutritional_anamnesis'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(ForeignKey('nutrifoods.consultation.id'), primary_key=True)
    created_on = Column(DateTime(True), server_default=text("(now())::timestamp without time zone"))
    last_updated = Column(DateTime(True), server_default=text("(now())::timestamp without time zone"))


t_daily_menu_nutritional_target = Table(
    'daily_menu_nutritional_target', metadata,
    Column('daily_menu_id', ForeignKey('nutrifoods.daily_menu.id'), primary_key=True, nullable=False),
    Column('nutritional_target_id', ForeignKey('nutrifoods.nutritional_target.id'), primary_key=True, nullable=False),
    schema='nutrifoods'
)


t_daily_menu_nutritional_value = Table(
    'daily_menu_nutritional_value', metadata,
    Column('daily_menu_id', ForeignKey('nutrifoods.daily_menu.id'), primary_key=True, nullable=False),
    Column('nutritional_value_id', ForeignKey('nutrifoods.nutritional_value.id'), primary_key=True, nullable=False),
    schema='nutrifoods'
)


class MenuRecipe(Base):
    __tablename__ = 'menu_recipe'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('nutrifoods.menu_recipe_id_seq'::regclass)"))
    daily_menu_id = Column(ForeignKey('nutrifoods.daily_menu.id'), nullable=False)
    recipe_id = Column(ForeignKey('nutrifoods.recipe.id'), nullable=False)
    portions = Column(Integer, nullable=False)

    daily_menu = relationship('DailyMenu')
    recipe = relationship('Recipe')


class RecipeMeasure(Base):
    __tablename__ = 'recipe_measure'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('nutrifoods.recipe_measure_id_seq'::regclass)"))
    recipe_id = Column(ForeignKey('nutrifoods.recipe.id'), nullable=False)
    ingredient_measure_id = Column(ForeignKey('nutrifoods.ingredient_measure.id'), nullable=False)
    integer_part = Column(Integer, nullable=False)
    numerator = Column(Integer, nullable=False)
    denominator = Column(Integer, nullable=False)

    ingredient_measure = relationship('IngredientMeasure')
    recipe = relationship('Recipe')


t_meal_plan = Table(
    'meal_plan', metadata,
    Column('consultation_id', ForeignKey('nutrifoods.consultation.id'), primary_key=True, nullable=False),
    Column('daily_plan_id', ForeignKey('nutrifoods.daily_plan.id'), primary_key=True, nullable=False),
    schema='nutrifoods'
)


class AdverseFoodReaction(Base):
    __tablename__ = 'adverse_food_reaction'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(UUID, primary_key=True, server_default=text("nutrifoods.uuid_generate_v4()"))
    food_group = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    nutritional_anamnesis_id = Column(ForeignKey('nutrifoods.nutritional_anamnesis.id'), nullable=False)

    nutritional_anamnesis = relationship('NutritionalAnamnesi')


class ClinicalSign(Base):
    __tablename__ = 'clinical_sign'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(UUID, primary_key=True, server_default=text("nutrifoods.uuid_generate_v4()"))
    name = Column(String(64), nullable=False)
    observations = Column(Text, server_default=text("''::text"))
    clinical_anamnesis_id = Column(ForeignKey('nutrifoods.clinical_anamnesis.id'), nullable=False)

    clinical_anamnesis = relationship('ClinicalAnamnesi')


class Disease(Base):
    __tablename__ = 'disease'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(UUID, primary_key=True, server_default=text("nutrifoods.uuid_generate_v4()"))
    name = Column(String(64), nullable=False)
    inheritance_types = Column(ARRAY(Integer()), nullable=False, server_default=text("ARRAY[]::integer[]"))
    clinical_anamnesis_id = Column(ForeignKey('nutrifoods.clinical_anamnesis.id'), nullable=False)

    clinical_anamnesis = relationship('ClinicalAnamnesi')


class EatingSymptom(Base):
    __tablename__ = 'eating_symptom'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(UUID, primary_key=True, server_default=text("nutrifoods.uuid_generate_v4()"))
    name = Column(String(64), nullable=False)
    observations = Column(Text, server_default=text("''::text"))
    nutritional_anamnesis_id = Column(ForeignKey('nutrifoods.nutritional_anamnesis.id'), nullable=False)

    nutritional_anamnesis = relationship('NutritionalAnamnesi')


class FoodConsumption(Base):
    __tablename__ = 'food_consumption'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(UUID, primary_key=True, server_default=text("nutrifoods.uuid_generate_v4()"))
    food_group = Column(Integer, nullable=False)
    frequency = Column(Integer, nullable=False)
    nutritional_anamnesis_id = Column(ForeignKey('nutrifoods.nutritional_anamnesis.id'), nullable=False)

    nutritional_anamnesis = relationship('NutritionalAnamnesi')


class HarmfulHabit(Base):
    __tablename__ = 'harmful_habit'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(UUID, primary_key=True, server_default=text("nutrifoods.uuid_generate_v4()"))
    name = Column(String(64), nullable=False)
    observations = Column(Text, server_default=text("''::text"))
    nutritional_anamnesis_id = Column(ForeignKey('nutrifoods.nutritional_anamnesis.id'), nullable=False)

    nutritional_anamnesis = relationship('NutritionalAnamnesi')


class Ingestible(Base):
    __tablename__ = 'ingestible'
    __table_args__ = {'schema': 'nutrifoods'}

    id = Column(UUID, primary_key=True, server_default=text("nutrifoods.uuid_generate_v4()"))
    name = Column(String(64), nullable=False)
    type = Column(Integer, nullable=False)
    administration_times = Column(ARRAY(String(length=8)), nullable=False, server_default=text("ARRAY[]::character varying[]"))
    dosage = Column(Integer)
    unit = Column(Integer)
    adherence = Column(Integer, nullable=False)
    observations = Column(Text, server_default=text("''::text"))
    clinical_anamnesis_id = Column(ForeignKey('nutrifoods.clinical_anamnesis.id'), nullable=False)

    clinical_anamnesis = relationship('ClinicalAnamnesi')
