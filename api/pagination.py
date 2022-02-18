from rest_framework import pagination

class PageNumberPaginationWithCount(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        response = super(PageNumberPaginationWithCount, self).get_paginated_response(data)
        response.data['total_pages'] = self.page.paginator.num_pages
        return response

def PageNumberPaginationWithCount_PageSize(_page_size = 10):
    class PageNumberPaginationWithCount_Sized(pagination.PageNumberPagination):
        page_size = _page_size
        def get_paginated_response(self, data):
            response = super(PageNumberPaginationWithCount_Sized, self).get_paginated_response(data)
            response.data['total_pages'] = self.page.paginator.num_pages
            return response
    return PageNumberPaginationWithCount_Sized