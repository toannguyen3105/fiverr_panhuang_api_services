#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import db
from utils.date_format import getTimeStringFromTimeStamp
from sqlalchemy import desc


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, comment="Item name")
    description = db.Column(db.String(500), nullable=False, comment="Item description")
    price = db.Column(db.Float(precision=2), nullable=False, comment="Item price")
    status = db.Column(db.Integer, default=1, nullable=True, comment="1 is active, 0 inactive")
    created_at = db.Column(db.Integer, nullable=True, comment="Timestamp")
    created_by = db.Column(db.String(30), nullable=True, comment="Timestamp")
    updated_at = db.Column(db.Integer, nullable=True, comment="Timestamp")
    updated_by = db.Column(db.String(30), nullable=True, comment="Timestamp")

    def __init__(self, name, description, price, status, created_at, created_by, updated_at, updated_by):
        self.name = name
        self.description = description
        self.price = price
        self.status = status
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'status': self.status,
            'created_at': self.created_at,
            'created_at_string': None if self.created_at is None else getTimeStringFromTimeStamp(self.created_at),
            'created_by': self.created_by,
            'updated_at': self.updated_at,
            'updated_at_string': None if self.updated_at is None else getTimeStringFromTimeStamp(self.updated_at),
            'updated_by': self.updated_by
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, _name):
        return cls.query.filter_by(name=_name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.order_by(desc(cls.created_at)).all()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
