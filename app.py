from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(20))
    lists = db.relationship("List", backref="category", cascade="all, delete, delete-orphan")

    def __init__(self, category_name):
        self.category_name = category_name

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_name = db.Column(db.String(20))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    items = db.relationship("Item", backref="list", cascade="all, delete, delete-orphan")

    def __init__(self, list_name, category_id):
        self.list_name = list_name
        self.category_id = category_id

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(30), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey("list.id"), nullable=False)

    def __init__(self, item_name, list_id):
        self.item_name = item_name
        self.list_id = list_id


class ItemSchema(ma.Schema):
    class Meta:
        fields = ("id", "item_name")

item_schema = ItemSchema()
multi_item_schema = ItemSchema(many=True)

class ListSchema(ma.Schema):
    class Meta:
        fields = ("id", "list_name", "items")
    items = ma.Nested(multi_item_schema)

list_schema = ListSchema()
multi_list_schema = ListSchema(many=True)

class CategorySchema(ma.Schema):
    class Meta:
        fields = ("id", "category_name", "lists")
    lists = ma.Nested(multi_list_schema)

category_schema = CategorySchema()
multi_category_schema = CategorySchema(many=True)















if __name__ == "__main__":
    app.run(debug=True)