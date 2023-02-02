import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

import row_data

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(255))
    role = db.Column(db.String(255))
    phone = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
        }


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    start_date = db.Column(db.String())
    end_date = db.Column(db.String())
    address = db.Column(db.String(255))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id,
        }


class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
        }


# ---------------------------------User Views----------------------------------

@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        result = []
        for u in User.query.all():
            result.append(u.to_dict())
        return json.dumps(result), 200

    if request.method == "POST":
        user_data = json.loads(request.data)
        new_user = User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"],
        )
        db.session.add(new_user)
        db.session.commit()

        return "User created", 201


@app.route("/users/<int:uid>", methods=["GET", "PUT", "DELETE"])
def user(uid: int):
    if request.method == "GET":
        return json.dumps(User.query.get(uid).to_dict()), 200
    if request.method == "PUT":
        user_data = json.loads(request.data)
        u = User.query.get(uid)
        u.first_name = user_data["first_name"]
        u.last_name = user_data["last_name"]
        u.age = user_data["age"]
        u.email = user_data["email"]
        u.role = user_data["role"]
        u.phone = user_data["phone"]

        db.session.add(u)
        db.session.commit()

        return "User updated", 204

    if request.method == "DELETE":
        u = User.query.get(uid)
        db.session.delete(u)
        db.session.commit()

        return "User Delete", 204


# ---------------------------------Orders Views--------------------------

@app.route("/order", methods=["GET", "POST"])
def orders():
    if request.method == "GET":
        result = []
        for u in Order.query.all():
            result.append(u.to_dict())
        return json.dumps(result), 200

    if request.method == "POST":
        order_data = json.loads(request.data)
        new_order = User(
            id=order_data["id"],
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["end_date"],
            address=order_data["address"],
            price=order_data["price"],
            costumer_id=order_data["costumer_id"],
            executor_id=order_data["executor_id"],
        )

        db.session.add(new_order)
        db.session.commit()

        return "Order created", 201


@app.route("/order/<int:uid>", methods=["GET", "PUT", "DELETE"])
def order(uid: int):
    if request.method == "GET":
        return json.dumps(Order.query.get(uid).to_dict()), 200
    if request.method == "PUT":
        order_data = json.loads(request.data)
        u = Order.query.get(uid)
        u.name = order_data["name"]
        u.description = order_data["description"]
        u.start_date = order_data["start_date"]
        u.end_date = order_data["end_date"]
        u.address = order_data["address"]
        u.price = order_data["price"]
        u.costumer_id = order_data["costumer_id"]
        u.executor_id = order_data["executor_id"]

        db.session.add(u)
        db.session.commit()

        return "Order updated", 204

    if request.method == "DELETE":
        u = Order.query.get(uid)
        db.session.delete(u)
        db.session.commit()

        return "Order Delete", 204


# -------------------------------Offers views-----------------------------
@app.route("/offer", methods=["GET", "POST"])
def offer():
    if request.method == "GET":
        result = []
        for u in Offer.query.all():
            result.append(u.to_dict())
        return json.dumps(result), 200

    if request.method == "POST":
        offer_data = json.loads(request.data)
        new_offer = Offer(
            id=offer_data["id"],
            order_id=offer_data["order_id"],
            executor_id=offer_data["executor_id"],
        )

        db.session.add(new_offer)
        db.session.commit()

    return "Offer created", 201


@app.route("/offer/<int:uid>", methods=["GET", "PUT", "DELETE"])
def offers(uid: int):
    if request.method == "GET":
        return json.dumps(Offer.query.get(uid).to_dict()), 200

    if request.method == "PUT":
        offer_data = json.loads(request.data)
        u = Offer.query.get(uid)
        u.order_id = offer_data["order_id"],
        u.executor_id = offer_data["executor_id"],

        db.session.add(u)
        db.session.commit()

        return "Offer updated"
    if request.method == "DELETE":
        u = Offer.query.get(uid)
        db.session.delete(u)
        db.session.commit()

        return "Offer delete", 204


# ---------------------------------Init----------------------------------

def init_database():
    db.drop_all()
    db.create_all()

    for user_data in row_data.users:
        new_user = User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"],
        )

        db.session.add(new_user)
        db.session.commit()

    for order_data in row_data.orders:
        new_order = Order(
            id=order_data["id"],
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["end_date"],
            address=order_data["address"],
            price=order_data["price"],
            costumer_id=order_data["costumer_id"],
            executor_id=order_data["executor_id"],
        )

        db.session.add(new_order)
        db.session.commit()

    for offer_data in row_data.offers:
        new_offer = Offer(
            id=offer_data["id"],
            order_id=offer_data["executor_id"],
            executor_id=offer_data["executor_id"],
        )

        db.session.add(new_offer)
        db.session.commit()


if __name__ == '__main__':
    init_database()
    app.run(debug=True)
