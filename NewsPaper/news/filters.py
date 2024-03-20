from django_filters import FilterSet, DateFilter
from .models import Post
from django import forms


class PostFilter(FilterSet):
    date = DateFilter(field_name="post_time_in", widget=forms.DateInput(attrs={'type': "date"}),
                      label='Дата', lookup_expr='date__gte')

    class Meta:
        model = Post
        fields = {

            'post_title': ['icontains'],
            'author': ['in']

        }