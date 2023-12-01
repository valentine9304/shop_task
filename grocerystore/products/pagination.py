from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page = 10
    page_size = 10  # Установите необходимый размер страницы
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        total_sum = sum(item.get("sum", 0) for item in data)
        total_count = sum(item.get("quantity", 0) for item in data)
        return Response(
            {
                "total_sum": total_sum,
                "total_count": total_count,
                "results": data,
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            }
        )
