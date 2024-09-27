from marshmallow import Schema, fields


class CarOwnerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class CarSchema(Schema):
    id = fields.Int(dump_only=True)
    color = fields.Str(required=True)
    model = fields.Str(required=True)
    owner_id = fields.Int(required=True)


car_owner_schema = CarOwnerSchema()
car_schema = CarSchema()
