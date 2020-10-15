from rest_framework import serializers

from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["name"]


class BookListSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "authors",
            "publication_date",
            "isbn",
            "page_count",
            "cover_photo",
            "publication_language",
        )


class SearchBookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    author = serializers.CharField(max_length=30)
    isbn = serializers.CharField(max_length=30)
    general = serializers.CharField(max_length=50)


class SearchBookResultsListSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    authors = serializers.CharField(max_length=100)
    isbn = serializers.CharField(max_length=20)
    publication_language = serializers.CharField(max_length=10)
    publication_date = serializers.DateField()
    cover_photo_url = serializers.URLField(max_length=100)
    page_count = serializers.IntegerField()


class BookCreateSerializer(serializers.ModelSerializer):
    authors = serializers.CharField(max_length=100)

    class Meta:
        model = Book
        fields = (
            "title",
            "authors",
            "publication_date",
            "isbn",
            "page_count",
            "cover_photo",
            "publication_language",
        )
