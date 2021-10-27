#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import db
from utils.date_format import getTimeStringFromTimeStamp
from sqlalchemy import desc


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True, comment="Username")
    password = db.Column(db.String(80), nullable=False, comment="Password")
    status = db.Column(db.Integer, default=1, nullable=True, comment="1 is active, 0 inactive")
    created_at = db.Column(db.Integer, nullable=True, comment="Timestamp")
    created_by = db.Column(db.String(30), nullable=True, comment="Timestamp")
    updated_at = db.Column(db.Integer, nullable=True, comment="Timestamp")
    updated_by = db.Column(db.String(30), nullable=True, comment="Timestamp")

    def __init__(self, username, password, status, created_at, created_by, updated_at, updated_by):
        self.username = username
        self.password = password
        self.status = status
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'status': self.status,
            'created_at': self.created_at,
            'created_at_string': None if self.created_at is None else getTimeStringFromTimeStamp(self.created_at),
            'created_by': self.created_by,
            'updated_at': self.updated_at,
            'updated_at_string': None if self.updated_at is None else getTimeStringFromTimeStamp(self.updated_at),
            'updated_by': self.updated_by
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.order_by(desc(cls.created_at)).all()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
