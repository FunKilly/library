from django_filters import FilterSet
from django_filters.rest_framework import FilterSet, filters
from django_filters.widgets import RangeWidget

from .models import Book


class BaseBookFilter(FilterSet):
    publication_date = filters.DateFromToRangeFilter(field_name="publication_date")
    authors = filters.Filter(field_name="authors__name", lookup_expr="icontains")

    class Meta:
        model = Book
        fields = {
            "title": ["icontains"],
            "publication_language": ["icontains"],
        }


class ApiBookFilter(BaseBookFilter):
    pass


class BookFilter(BaseBookFilter):
    publication_date = filters.DateFromToRangeFilter(
        field_name="publication_date",
        widget=RangeWidget(attrs={"placeholder": "YYYY-MM-DD"}),
    )
