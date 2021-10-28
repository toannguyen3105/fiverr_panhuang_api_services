#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.item import ItemModel

from utils.date_format import getTimeStamp
from utils.response import generate_response


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name",
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument("description",
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def post(self):
        data = self.parser.parse_args()

        name = data["name"]
        description = data["description"]
        price = data["price"]
        status = 0

        item = ItemModel(name, description, price, status, getTimeStamp(), None, None, None)
        item.save_to_db()

        return generate_response(None, 0, item.json(), 201)


class ItemList(Resource):
    @jwt_required()
    def get(self):
        items = [item.json() for item in ItemModel.find_all()]
        return {
                   "message": "List item",
                   "data": items,
                   "total": len(ItemModel.find_all())
               }, 200


class ItemUpdateStatus(Resource):
    @jwt_required()
    def put(self, item_id: int):
        item = ItemModel.find_by_id(item_id)
        if item is None:
            return generate_response(None, 4, None, 404)

        item.status = 1
        item.updated_at = getTimeStamp()
        item.updated_by = "ADMIN"

        item.save_to_db()

        return generate_response(None, 0, item.json(), 200)
