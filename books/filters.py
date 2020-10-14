from django.db.models import Q

from django_filters.rest_framework import FilterSet, filters
from django_filters.widgets import RangeWidget
from django_filters import FilterSet

from .models import Book


class ApiBookFilter(FilterSet):
    author = filters.CharFilter(field_name="author", method="filter_by_full_name")
    publication_date = filters.DateFromToRangeFilter(field_name="publication_date")

    class Meta:
        model = Book
        fields = ("title", "publication_language")

    def filter_by_full_name(self, qs, name, value):
        for term in value.split():
            qs = qs.filter(
                Q(author__name__icontains=term) | Q(author__surname__icontains=term)
            )
        return qs


class BookFilter(FilterSet):
    author = filters.CharFilter(field_name="author", method="filter_by_full_name")
    publication_date = filters.DateFromToRangeFilter(field_name="publication_date", widget=RangeWidget(attrs={'placeholder': 'YYYY-MM-DD'}))

    class Meta:
        model = Book
        fields = ("title", "publication_language")

    def filter_by_full_name(self, qs, name, value):
        for term in value.split():
            qs = qs.filter(
                Q(author__name__icontains=term) | Q(author__surname__icontains=term)
            )
        return qs

