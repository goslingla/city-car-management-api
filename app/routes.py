from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from .models import db, CarOwner, Car
from .schemas import car_owner_schema, car_schema

api = Blueprint("api", __name__)


@api.route("/login", methods=["POST"])
def login():
    # Simplificado para demonstração. Em produção, verifique as credenciais.
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "admin" or password != "password":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@api.route("/car_owners", methods=["GET"])
@jwt_required()
def get_car_owners():
    owners = CarOwner.query.all()
    return jsonify(car_owner_schema.dump(owners, many=True)), 200


@api.route("/car_owners", methods=["POST"])
@jwt_required()
def add_car_owner():
    data = request.json
    new_owner = CarOwner(name=data["name"])
    db.session.add(new_owner)
    db.session.commit()
    return car_owner_schema.dump(new_owner), 201


@api.route("/cars", methods=["GET"])
@jwt_required()
def get_cars():
    cars = Car.query.all()
    return jsonify(car_schema.dump(cars, many=True)), 200


@api.route("/cars", methods=["POST"])
@jwt_required()
def add_car():
    data = request.json
    owner = CarOwner.query.get(data["owner_id"])
    if not owner:
        return jsonify({"message": "Owner not found"}), 404
    if len(owner.cars) >= 3:
        return jsonify({"message": "Owner already has 3 cars"}), 400
    if data["color"] not in ["yellow", "blue", "gray"]:
        return jsonify({"message": "Invalid color"}), 400
    if data["model"] not in ["hatch", "sedan", "convertible"]:
        return jsonify({"message": "Invalid model"}), 400
    new_car = Car(color=data["color"], model=data["model"], owner_id=data["owner_id"])
    db.session.add(new_car)
    db.session.commit()
    return car_schema.dump(new_car), 201
