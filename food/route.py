from datetime import date

from flask import Blueprint, current_app, request

from core import ActionType
from .data import get_data, add_food, to_json, remove_food, get_food

food_route = Blueprint('food_route', __name__)


@food_route.route('/', methods=['GET'])
def food_lst() -> object:
    data = get_data()
    current_app.logger.info('Get all data: {0}'.format(data))
    return to_json(data)


@food_route.route('/<action_type:action>', methods=['POST'])
def food_action(action: ActionType):
    logger = current_app.logger
    logger.info('Action: {0}'.format(action))
    data = request.get_json()
    logger.info('Got data: {0}'.format(data))
    if action == ActionType.ADD:
        add_food(name=data['name'], expire_date=date.fromisoformat(data['expire_date']), quantity=data['quantity'])
    if action == ActionType.REMOVE:
        remove_food(name=data['name'], expire_date=date.fromisoformat(data['expire_date']), quantity=data['quantity'])

    try:
        food = get_food(name=data['name'])
        return to_json(food)
    except ValueError:
        return ''
