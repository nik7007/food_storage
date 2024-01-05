from enum import unique, Enum

from werkzeug.routing import BaseConverter, ValidationError


@unique
class ActionType(str, Enum):
    ADD = 'add'
    REMOVE = 'remove'


class ActionTypeConverter(BaseConverter):
    def to_python(self, value):
        try:
            request_type = ActionType(value)
            return request_type
        except ValueError:
            raise ValidationError()

    def to_url(self, obj):
        return obj.value
