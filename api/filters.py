import django_filters
from django_filters.constants import EMPTY_VALUES
from .models import *


class ListFilter(django_filters.Filter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        value_list = value.split(",")
        qs = super().filter(qs, value_list)
        return qs

# use to filter data
class DailyPriceFilter(django_filters.FilterSet):
    date = django_filters.DateFilter()
    date__gte = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date__lte = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    symbol = ListFilter(lookup_expr="in")
    class Meta:
        model = DailyPriceModel
        fields = '__all__'