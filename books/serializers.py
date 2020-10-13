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
        return f"{obj.author.name} {obj.author.surname}"
