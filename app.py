from os import abort

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://myuser:123A@localhost/iot_test_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Shoes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Integer, unique=False)
    season = db.Column(db.String(10), unique=False)

    def __init__(self, size, season):
        self.size = size
        self.season = season


class ShoesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'size', 'season')


shoes_schema = ShoesSchema()
multiple_shoes_schema = ShoesSchema(many=True)
db.create_all()


@app.route("/shoes", methods=["GET"])
def get_shoes():
    all_shoes = Shoes.query.all()
    result = multiple_shoes_schema.dump(all_shoes)
    return jsonify(result)


@app.route("/shoes/<id>", methods=["GET"])
def shoes_by_id(id):
    shoe = Shoes.query.get(id)
    if not shoe:
        abort(404)
    return jsonify(shoes_schema.dump(shoe))


@app.route("/shoes", methods=["POST"])
def add_tool():
    new_shoes = Shoes(size=request.json["size"], season=request.json["season"])
    db.session.add(new_shoes)
    db.session.commit()
    return jsonify(shoes_schema.dump(new_shoes))


@app.route("/shoes/<id>", methods=["PUT"])
def tool_update(id):
    shoe = Shoes.query.get(id)
    if not shoe:
        abort(404)
    shoe.size = request.json["size"]
    shoe.producer = request.json["season"]
    db.session.commit()
    return jsonify(success=True)


@app.route("/shoes/<id>", methods=["DELETE"])
def tool_delete(id):
    shoe = Shoes.query.get(id)
    if not shoe:
        abort(404)
    db.session.delete(shoe)
    db.session.commit()
    return jsonify(success=True)


if __name__ == '__main__':
    app.run(debug=True)
