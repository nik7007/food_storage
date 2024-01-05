import json
import os
from datetime import date

from .model import Food, FoodSchema

FOOD_DATA_FILE = 'out/food_data.json'

data: list[Food] | None = None


def get_data() -> list[Food]:
    global data
    if data is None:
        try:
            with open(FOOD_DATA_FILE, 'r') as f:
                raw_data = json.load(f)
            schema = FoodSchema(many=True)
            data = schema.load(raw_data)
        except Exception:
            data = []
    return data


def get_food(name: str) -> Food:
    foods = get_data()
    food = next((food for food in foods if food.name == name), None)
    if food is not None:
        return food
    else:
        raise ValueError(f"Food with name '{name}' not found")


def to_json(foods: list[Food] | Food) -> object:
    many = type(foods) is list
    schema = FoodSchema(many=many)
    return schema.dump(foods)


def update_data(foods: list[Food]) -> None:
    foods_dump = to_json(foods)
    os.makedirs(os.path.dirname(FOOD_DATA_FILE), exist_ok=True)
    with open(FOOD_DATA_FILE, 'w') as f:
        json.dump(foods_dump, f, ensure_ascii=False, indent=2)
    global data
    data = foods


def add_food(name: str, expire_date: date, quantity: int = 1) -> None:
    foods = get_data()
    filtered_foods = [food for food in foods if food.name == name]
    for ff in filtered_foods:
        ff.add_expire_date(expire_date, quantity)
        break
    else:
        food = Food(name, [])
        food.add_expire_date(expire_date, quantity)
        foods.append(food)
    update_data(foods)


def remove_food(name: str, expire_date: date, quantity: int = 1) -> None:
    foods = get_data()
    filtered_foods = [food for food in foods if food.name == name]
    for ff in filtered_foods:
        ff.remove_expire_date(expire_date, quantity)
        if ff.food_attributes is None or len(ff.food_attributes) == 0:
            foods.remove(ff)
    update_data(foods)
