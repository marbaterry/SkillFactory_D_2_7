from django_filters import FilterSet  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post

import django_filters
from django.forms import DateInput

# создаём фильтр
class PostFilter(FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Title contains')
    date = django_filters.DateFilter(field_name='date', widget=DateInput( attrs={'type': 'date'}),
                                         lookup_expr='gt', label='Greater than date')
    author = django_filters.CharFilter(field_name='author_id__authorUser_id__username', lookup_expr='icontains',
                                            label='Author')
