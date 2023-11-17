from django_filters import rest_framework as filters
from .models import *

class ProductFilters(filters.FilterSet):
    keywords = filters.CharFilter(field_name="name", lookup_expr="icontains")
    min_price = filters.CharFilter(field_name="price" or 0, lookup_expr="gle")
    max_price = filters.CharFilter(field_name="price" or 100000, lookup_expr='lte')
    class Meta():
        model = Product
        fields = ('category','ratings','keywords','min_price')