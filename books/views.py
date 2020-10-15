from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import ApiBookFilter, BookFilter
from .integrations import google_api
from .models import Book
from .serializers import (
    BookCreateSerializer,
    BookListSerializer,
    SearchBookResultsSerializer,
    SearchBookSerializer,
)


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


class BookCreateView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "book_create.html"

    def get(self, request):
        serializer = BookCreateSerializer()
        return Response({"serializer": serializer})

    def post(self, request):
        serializer = BookCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer})
        else:
            serializer.save()
            messages.success(request, "Your data has been saved!")
            context = {"serializer": BookCreateSerializer()}
            return render(request, "book_create.html", context)


class BookUpdateView(SuccessMessageMixin, UpdateView):
    model = Book
    template_name = "book_update.html"
    fields = "__all__"
    success_message = "Book has been updated successfully"

    def get_success_url(self):
        self.kwargs["pk"]
        return reverse_lazy("book-update", kwargs={"pk": self.kwargs["pk"]})


class BookDeleteView(DeleteView):
    model = Book
    template_name = "book_confirm_delete.html"
    fields = "__all__"
    success_url = reverse_lazy("book-list")


class ImportBookSearchView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "book_search.html"

    def get(self, request):
        serializer = SearchBookSerializer()
        return Response({"serializer": serializer})

    def post(self, request):
        template = loader.get_template("book_search_result.html")

        response = google_api.make_url_call(request.data)
        if response.get("items"):
            data = google_api.parse_response(response)
            serializer = SearchBookResultsSerializer(data, many=True)

            context = {"data": serializer.data}
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse(template.render({"data": []}, request))


class ImportBookSearchResultsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "book_search_result.html"

    def get(self, request):
        serializer = SearchBookResultsSerializer(request.data, many=True)
        return Response({"data": serializer})

    def post(self, request):

        return redirect("book-search-result-list", context={"data": serializer.data})


class RESTBookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ApiBookFilter
    search_fields = ["title", "author__name", "publication_language"]
