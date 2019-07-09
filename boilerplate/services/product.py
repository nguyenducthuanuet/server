import logging

_logger = logging.getLogger('main')
__author__ = 'Thuan Nguyen'

from boilerplate import models as m, repositories


class ProductListQuery(object):
    """
    Query danh sách sản phẩm theo 1 loạt các filter
    """

    def __init__(self):
        self.query = m.Product.query

    def __len__(self):
        """
        Trả về số lượng bản ghi tìm thấy
        :return:
        :rtype: int
        """
        return self.query.count()

    def __iter__(self):
        """
        Yield danh sách sản phẩm tìm thấy
        :return:
        :rtype: list[m.Product]
        """
        yield from self.query

    def apply_filters(self, **kwargs):
        """
        Filter theo các điều kiện được truyền vào, bao gồm:
            - từ khóa tìm kiếm (keyword)
            - brand (brand_id)
            - attribute set (attribute_set_id)
            - product line (product_line_id)
            - category (category_id)
            - selling status (selling_status)
            - editing status (editing_status)
            - objective (objective)
            - channel (channel_id)
            ...

        :param kwargs:
        :return:
        """
        keyword = kwargs.get('query')
        if keyword:
            self._apply_keyword_filter(keyword)
        self._apply_sort('id', 'desc')
        #
        # brand_id = kwargs.get('brandId')
        # if brand_id:
        #     self._apply_brand_filter(brand_id)
        #
        # attribute_set_id = kwargs.get('attributeSetId')
        # if attribute_set_id:
        #     self._apply_attribute_set_filter(attribute_set_id)
        #
        # product_line_id = kwargs.get('productLineId')
        # if product_line_id:
        #     self._apply_product_line_filter(product_line_id)
        #
        # category_id = kwargs.get('categoryId')
        # if category_id:
        #     self._apply_category_filter(category_id)
        #
        # selling_status = kwargs.get('sellingStatus')
        # if selling_status:
        #     self._apply_selling_status_filter(selling_status)
        #
        # editing_status = kwargs.get('editingStatus')
        # if editing_status:
        #     self._apply_editing_status_filter(editing_status)
        #
        # objective = kwargs.get('objective')
        # if objective:
        #     self._apply_objective_status_filter(objective)
        #
        # channel_id = kwargs.get('channelId')
        # if channel_id:
        #     self._apply_channel_filter(channel_id)
        #
        # is_bundle = kwargs.get('isBundle')
        # if is_bundle:
        #     self._apply_bundle_filter(is_bundle)

    def _apply_sort(self, sort_field, sort_order):
        sort_field = eval('m.Product.%s' % sort_field)
        if sort_order == 'ascend':
            sort_field = sort_field.asc()
        else:
            sort_field = sort_field.desc()
        self.query = self.query.order_by(sort_field)



    def _apply_keyword_filter(self, keyword):
        _like_expr = '%{}%'.format(keyword)
        self.query = self.query.filter(
            m.Product.name.like(_like_expr),
        )

    def paginate(self, page, page_size):
        """
        Apply pagination params to product list query
        :param page:
        :param page_size:
        :return:
        """
        page = page - 1 if page > 0 else 0
        self.query = self.query.offset(page * page_size).limit(page_size)


def get_product_list(**kwargs):
    """
    Return a list of product
    :param kwargs:
    :return:
    """
    list_query = ProductListQuery()
    list_query.apply_filters(**kwargs)
    page = kwargs.get('page', 0)
    page_size = kwargs.get('pageSize', 10)
    total_records = len(list_query)
    list_query.paginate(page, page_size)

    products = list(list_query)

    return {
        'current_page': page,
        'page_size': page_size,
        'total_items': total_records,
        'products': products
    }


def create_product(**kwargs):

    product = repositories.product.save_product_to_database(
        **kwargs
    )
    return product


def delete_product(product_id):
    product = m.Product.query.filter_by(id=product_id).first()
    repositories.product.delete_product(product)
