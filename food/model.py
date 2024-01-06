from datetime import date
from typing import Self

from marshmallow import Schema, fields, post_load


class FoodAttribute(object):
    def __init__(self, expire_date: date, quantity: int) -> None:
        self.expire_date = expire_date
        self.quantity = quantity


class Food(object):
    def __init__(self, name: str, food_attributes: list[FoodAttribute]) -> None:
        self.name = name
        self.food_attributes = food_attributes

    def add_expire_date(self, expire_date: date, quantity: int = 1) -> None:
        matching_attr = [x for x in self.food_attributes if x.expire_date == expire_date]
        for attr in matching_attr:
            attr.quantity += quantity
            break
        else:
            self.food_attributes.append(FoodAttribute(expire_date, quantity))

    def remove_expire_date(self, expire_date: date, quantity: int = 1) -> None:
        matching_attr = [x for x in self.food_attributes if x.expire_date == expire_date]
        for attr in matching_attr:
            attr.quantity -= quantity
            if attr.quantity <= 0:
                self.food_attributes.remove(attr)

    def expired_foods(self, expire_date: date) -> list[Self]:
        food_attributes = [FoodAttribute(attr.expire_date, attr.quantity) for attr in self.food_attributes if
                           attr.expire_date <= expire_date]
        if len(food_attributes) == 0:
            return list()
        return [Food(self.name, food_attributes)]


class FoodAction(object):
    def __init__(self, name: str, expire_date: date, quantity: int):
        self.name = name
        self.expire_date = expire_date
        self.quantity = quantity


# Schema for FoodAttribute class
class FoodAttributeSchema(Schema):
    # Fields should mirror attributes of FoodAttribute
    expire_date = fields.Date()
    quantity = fields.Int()

    # This decorator links loaded data with the corresponding class
    @post_load
    def make_object(self, data, **kwargs):
        return FoodAttribute(**data)


# Schema for Food class
class FoodSchema(Schema):
    # Fields should mirror attributes of Food
    name = fields.Str()
    food_attributes = fields.Nested(FoodAttributeSchema, many=True)

    # This decorator links loaded data with the corresponding class
    @post_load
    def make_object(self, data, **kwargs):
        return Food(**data)


class FoodActionSchema(Schema):
    name = fields.Str()
    expire_date = fields.Date()
    quantity = fields.Int()

    @post_load
    def make_object(self, data, **kwargs):
        return FoodAction(**data)
