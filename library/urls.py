"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from books.views import (
    BookCreateView,
    BookDeleteView,
    BookListView,
    BookSearchResultsImportView,
    BookSearchView,
    BookUpdateView,
    IndexView,
    RESTBookListView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("api/books", RESTBookListView.as_view(), name="rest_book_list"),
    path("books/", BookListView.as_view(), name="book_list"),
    path("books/add/", BookCreateView.as_view(), name="book_create"),
    path("books/<pk>/update", BookUpdateView.as_view(), name="book_update"),
    path("books/<pk>/delete", BookDeleteView.as_view(), name="book_delete"),
    path("books/search", BookSearchView.as_view(), name="book_search"),
    path(
        "books/search-result/<isbn>/add",
        BookSearchResultsImportView.as_view(),
        name="book_search_results_import",
    ),
]
