# coding=utf-8
import datetime
import enum
import logging

from flask_restplus import fields

from boilerplate.models import db, bcrypt, TimestampMixin

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)


class Product(db.Model, TimestampMixin):
    """
    Contains information of products table
    """
    __tablename__ = 'products'

    def __init__(self, **kwargs):
        """
        Support direct initialization
        :param kwargs:
        """
        for k, v in kwargs.items():
            setattr(self, k, v)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(191), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    sell_price = db.Column(db.String(255), nullable=True)
    import_price = db.Column(db.String(255), nullable=True)

    def get_id(self):
        return self.id

    def to_dict(self):
        """
        Transform user obj into dict
        :return:
        """
        return {
            'id': self.id,
            'name': self.username,
            'description': self.description,
            'sellPrice': self.sell_price,
            'importPrice': self.import_price
        }


class ProductSchema:
    product = {
        'id': fields.Integer(required=True, dzescription='product id'),
        'name': fields.String(required=True, description='product name'),
        'description': fields.String(required=False, description='product description'),
        'sell_price': fields.String(required=False, description='product sell price'),
        'import_price': fields.String(required=False, description='product Import price')
    }

    product_create_req = product.copy()
    product_create_req.pop('id', None)

    product_list_res = {
        'current_page': fields.Integer(required=True, description='Current page'),
        'page_size': fields.Integer(required=True, description='Page size'),
        'total_items': fields.Integer(required=True, description='Total items'),
        'products': fields.List(fields.Nested(product))
    }
