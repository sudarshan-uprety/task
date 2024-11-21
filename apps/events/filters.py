from django_filters import rest_framework as filters
from apps.events.models import Event


class EventFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='date', lookup_expr='lte')
    location = filters.CharFilter(field_name='location', lookup_expr='icontains')

    class Meta:
        model = Event
        fields = ['date_from', 'date_to', 'location']
