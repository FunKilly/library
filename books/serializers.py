from rest_framework import serializers

from .models import Book


class BookListSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author_name",
            "publication_date",
            "isbn",
            "page_count",
            "cover_photo",
            "publication_language",
        )

    def get_author_name(self, obj):
        return obj.author.name


class SearchBookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    author = serializers.CharField(max_length=30)
    isbn = serializers.CharField(max_length=30)
    general = serializers.CharField(max_length=50)


class SearchBookResultsSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    authors = serializers.CharField(max_length=100)
    isbn = serializers.CharField(max_length=20)
    publication_language = serializers.CharField(max_length=10)
    publication_date = serializers.DateField()
    cover_photo_url = serializers.CharField(max_length=100)
    page_count = serializers.IntegerField()


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "title",
            "author",
            "publication_date",
            "isbn",
            "page_count",
            "cover_photo",
            "publication_language",
        )
