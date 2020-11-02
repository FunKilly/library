from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from .filters import ApiBookFilter, BookFilter
from .forms import BookCreateForm, BookSearchForm, BookUpdateForm
from .integrations import google_api
from .models import Book
from .serializers import BookListSerializer


class IndexView(View):
    template_name = "index.html"

    def get(self, request):
        return render(request, self.template_name)


class BookListView(ListView):
    template_name = "book_list.html"
    model = Book
    context_object_name = "context"
    filter_fields = "__all__"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = BookFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        return context


class BookCreateView(CreateView):
    form_class = BookCreateForm
    template_name = "book_create.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            authors = form.cleaned_data.pop("authors")
            book = form.save()
            self.add_book(book, authors)
            messages.success(request, "Your book has been saved!")
            return redirect("book_list")
        else:
            return render(request, self.template_name, {"form": form})

    def add_book(self, book, authors):
        book.add_authors(authors)
        book.save()


class BookUpdateView(SuccessMessageMixin, UpdateView):
    model = Book
    form_class = BookUpdateForm
    template_name = "book_update.html"
    success_message = "Book has been updated successfully"

    def get_success_url(self):
        self.kwargs["pk"]
        return reverse_lazy("book_update", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        authors = form.cleaned_data.pop("authors")
        instance = form.save(commit=False)
        if authors:
            instance.add_authors(authors)
        return super(BookUpdateView, self).form_valid(form)


class BookDeleteView(DeleteView):
    model = Book
    template_name = "book_confirm_delete.html"
    fields = "__all__"
    success_url = reverse_lazy("book_list")


class BookSearchView(View):
    form_class = BookSearchForm
    template_name = "book_search.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            template = loader.get_template("book_search_result.html")
            books = self.get_books(form.cleaned_data)
            context = {"data": books}
            return HttpResponse(template.render(context, request))
        else:
            return render(request, self.template_name, {"form": form})

    def get_books(self, data):
        response = google_api.make_url_call(data)
        if response.get("items"):
            data = google_api.parse_response(response)
            return data
        else:
            return []


class BookSearchResultsImportView(View):
    def get(self, request, isbn):
        if not Book.objects.filter(isbn=isbn).exists():
            record = cache.get(isbn)
            if record:
                self.add_book(isbn, record)
                messages.success(request, "Your book has been saved!")
            else:
                messages.info(request, "Query results expired, please try again.")
        else:
            messages.info(request, "This book already exists in database.")
        return redirect("book_list")

    def add_book(self, isbn, record):
        book = Book.objects.create(
            title=record["title"],
            publication_date=record["publication_date"],
            isbn=isbn,
            page_count=record["page_count"],
            cover_photo=record["cover_photo_url"],
            publication_language=record["publication_language"],
        )
        book.add_authors(record["authors"])
        book.save()


class RESTBookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ApiBookFilter
    search_fields = ["title", "authors__name", "publication_language"]
