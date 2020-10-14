from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from .filters import BooksFilter
from .models import Book
from .serializers import BookListSerializer


class BookListView(ListView):
    model = Book
    template_name = "book_list.html"
    paginate_by = 5


class BookCreateView(SuccessMessageMixin, CreateView):
    model = Book
    template_name = "book_create.html"
    fields = "__all__"
    success_url = reverse_lazy('book-create')
    success_message = "Book has been added successfully"


class BookUpdateView(SuccessMessageMixin, UpdateView):
    model = Book
    template_name = "book_update.html"
    fields = "__all__"
    success_message = "Book has been updated successfully"

    def get_success_url(self):
          companyid=self.kwargs['pk']
          return reverse_lazy('book-update', kwargs={'pk': self.kwargs['pk']})
    

class BookDeleteView(DeleteView):
    model = Book
    template_name = "book_confirm_delete.html"
    fields = "__all__"
    success_url = reverse_lazy('book-list')


class RESTBookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = BooksFilter
    search_fields = ["title", "author__name", "author__surname", "publication_language"]
