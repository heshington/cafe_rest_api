from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

from random import randint

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
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


@app.route("/")
def home():
    return render_template("index.html")


## HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def random():
    all_cafes = db.session.query(Cafe).all()
    random_num = randint(0, len(all_cafes))
    chosen_cafe = all_cafes[random_num]
    return jsonify(name=chosen_cafe.name,
                   map_url=chosen_cafe.map_url,
                   img_url=chosen_cafe.img_url,
                   location=chosen_cafe.location,
                   has_sockets=chosen_cafe.has_sockets,
                   has_toilet=chosen_cafe.has_toilet,
                   has_wifi=chosen_cafe.has_wifi,
                   can_take_calls=chosen_cafe.can_take_calls,
                   seats=chosen_cafe.seats,
                   coffee_price=chosen_cafe.coffee_price)


@app.route("/all", methods=["GET"])
def all():
    cafes = db.session.query(Cafe).all()
    all_cafes = []
    for cafe in cafes:
        cafe_dict = cafe.to_dict()
        print(cafe_dict)
        all_cafes.append(cafe_dict)
    print(all_cafes)

    return jsonify(cafes=all_cafes)


@app.route("/search", methods=["GET"])
def search():
    search_term = request.args.get('location')
    cafes = db.session.query(Cafe).all()
    matched_cafes = []
    for cafe in cafes:
        if cafe.location == search_term:
            cafe_dict = cafe.to_dict()
            matched_cafes.append(cafe_dict)

    if matched_cafes:
        return jsonify(matched_cafes)
    else:
        return jsonify({"error": {
            "Not Found": "Sorry, we don't have a cafe at that location."
        }})
def make_bool(val: int) -> bool:
    return bool(int(val))

## HTTP POST - Create Record
@app.route("/add", methods=['POST'])
def add():
    new_cafe = Cafe(
        name=request.form.get('name'),
        map_url=request.form.get('map_url'),
        img_url=request.form.get('img_url'),
        location=request.form.get('location'),
        seats=request.form.get('seats'),
        has_toilet=make_bool(request.form.get('has_toilet')),
        has_wifi=make_bool(request.form.get('has_wifi')),
        has_sockets=make_bool(request.form.get('has_sockets')),
        can_take_calls=make_bool(request.form.get('can_take_calls')),
        coffee_price=request.form.get('coffee_price'),
    )

    # add to the database
    print("Printing the new cafe's name...")
    print(new_cafe.name)
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"Success": "Successfully added the new cafe."})


## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
