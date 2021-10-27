#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from flask_restful import Resource, reqparse
from hmac import compare_digest
from flask_jwt_extended import (create_access_token, create_refresh_token)

from models.user import UserModel
from utils.date_format import getTimeStamp
from utils.response import generate_response

STATUS_CODES = ['OK', 'INTERNAL_ERROR', 'DATABASE_ERROR']


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = self.parser.parse_args()

        username = data["username"]
        if UserModel.find_by_username(username):
            return generate_response("Yes", 3, None, 400)
        else:
            password = data["password"]
            status = 1
            user = UserModel(username, password, status, getTimeStamp(), None, None, None)
            user.save_to_db()

            return generate_response(None, 0, None, 201)


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = self.parser.parse_args()

        password = data['password']
        user = UserModel.find_by_username(data["username"])
        if user and compare_digest(user.password, password):
            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=user.id, expires_delta=expires, fresh=True)
            refresh_token = create_refresh_token(user.id)

            result = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            return generate_response(None, 0, result, 200)

        return generate_response("Yes", 1, None, 400)
