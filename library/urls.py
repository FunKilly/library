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
    BookUpdateView,
    ImportBookSearchResultsView,
    ImportBookSearchView,
    RESTBookListView,
)

urlpatterns = [
    path("api/books", RESTBookListView.as_view(), name="rest-book-list"),
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/add/", BookCreateView.as_view(), name="book-create"),
    path("books/<pk>/update", BookUpdateView.as_view(), name="book-update"),
    path("books/<pk>/delete", BookDeleteView.as_view(), name="book-delete"),
    path("books/search", ImportBookSearchView.as_view(), name="book-search"),
    path(
        "books/search-result",
        ImportBookSearchResultsView.as_view(),
        name="book-search-result-list",
    ),
]
