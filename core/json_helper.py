from marshmallow import Schema


def to_json_with_schema[T](data: list[T] | T, schema_class: type[Schema]) -> object:
    many = type(data) is list
    schema = schema_class(many=many)
    return schema.dump(data)
