from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from .filters import BooksFilter
from .models import Book
from .serializers import BookListSerializer


class RESTBookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = BooksFilter
    search_fields = ["title", "author__name", "author__surname", "publication_language"]
