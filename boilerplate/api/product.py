from boilerplate.extensions.reqparse import RequestParser

__author__ = 'Thuan Nguyen'
import logging

from boilerplate.extensions import Namespace
from boilerplate import services, models
import flask_restplus as _fr
from flask import request

_logger = logging.getLogger(__name__)
ns = Namespace('products', description='Products operations')

_product_res = ns.model('product_res', models.ProductSchema.product)
_product_create_req = ns.model('product_create_req', models.ProductSchema.product_create_req)
_product_list_res = ns.model('product_list_res', models.ProductSchema.product_list_res)

product_list_params = RequestParser(bundle_errors=True)
product_list_params.add_argument('page', type=int, help='Page number, start from 1', required=False, default=1,
                                 location='args')
product_list_params.add_argument('pageSize', type=int,
                                 help='Page size',
                                 required=False, default=10, location='args')
product_list_params.add_argument('query', type=str,
                                 help='Query name or sku',
                                 required=False, location='args')


@ns.route('/', methods=['GET', 'POST', 'DELETE'])
class Product(_fr.Resource):
    @ns.expect(_product_create_req, validate=True)
    @ns.marshal_with(_product_res)
    def post(self):
        """
        Create new user
        :return: list[User]
        """
        data = request.json
        product = services.product.create_product(**data)
        return product

    @ns.marshal_with(_product_list_res)
    def get(self):
        args = product_list_params.parse_args()
        res = services.product.get_product_list(**args)
        return res

    def delete(self):
        data = request.json
        id = data.get('id')
        if id:
            services.product.delete_product(id)
        return {}
