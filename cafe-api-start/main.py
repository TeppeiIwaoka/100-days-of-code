from random import random, choice

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random", methods=["GET", "POST"])
def get_random_cafe():
    if request.method == "GET":
        cafes = db.session.query(Cafe).all()
        random_cafe = choice(cafes)
        return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all_cafe():
    cafes = db.session.query(Cafe).all()
    cafe_list = [cafe.to_dict() for cafe in cafes]
    return jsonify(cafes=cafe_list)


@app.route("/search")
def search_cafe():
    location = request.args.get("loc")
    target_cafes = db.session.query(Cafe).filter_by(location=location).all()
    if len(target_cafes) == 0:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at the location."})
    return jsonify(cafes=[cafe.to_dict() for cafe in target_cafes])


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    new_cafe = Cafe(
        name=request.args.get("name"),
        map_url=request.args.get("map_url"),
        location=request.args.get("loc"),
        has_sockets=request.args.get("sockets"),
        has_toilet=request.args.get("toilet"),
        has_wifi=request.args.get("wifi"),
        can_take_calls=request.args.get("calls"),
        seats=request.args.get("seats"),
        coffee_price=request.args.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit
    return jsonify(response={"success": "Successfully added the new cafe."})


@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = db.session.query(Cafe).get(cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def delete(cafe_id):
    if not request.args.get("api_key") == "TopSecretAPIKey":
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403

    cafe_to_be_deleted = db.session.query(Cafe).get(cafe_id)
    if cafe_to_be_deleted:
        db.session.delete(cafe_to_be_deleted)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted."}), 200
    else:
        return jsonify(error={"Not found": "Sorry a cafe with that id was not found in the database."}), 404


if __name__ == '__main__':
    app.run(debug=True)
