# coding=utf-8
import logging

from sqlalchemy import or_

from boilerplate import models as m

__author__ = 'Kien'
_logger = logging.getLogger(__name__)


def save_product_to_database(**kwargs):
    """
    Create new product record in database from validated data.
    :param kwargs:
    :return:
    """
    product = m.Product(**kwargs)
    m.db.session.add(product)

    return product


def delete_product(product):
    m.db.session.delete(product)
    m.db.session.commit()
