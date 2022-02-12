from typing import OrderedDict
from drf_yasg import openapi
from drf_yasg.inspectors import PaginatorInspector

class PageNumberPaginationWithCountInspector(PaginatorInspector):
    # open api scheme generation helper
    def get_paginated_response(self, paginator, response_schema):
        '''
        :param PageNumberPaginationWithCount paginator: the paginator
        :param openapi.Schema response_schema: the response schema that must be paged.
        :rtype: openapi.Schema
        '''
        child_item_ref = response_schema['items']['$ref']
        item_ref_title = child_item_ref.split('/')[-1]
        
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=OrderedDict((
                ('count', openapi.Schema(type=openapi.TYPE_INTEGER)),
                ('total_pages', openapi.Schema(type=openapi.TYPE_INTEGER)),
                ('next', openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, x_nullable=True)),
                ('previous', openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, x_nullable=True)),
                ('results', response_schema),
            )),
            required=['results'],
            title='Paged'+item_ref_title,
            description=f'Show paged results of {item_ref_title}'
        )