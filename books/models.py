import uuid

from django.db import models


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40, blank=False, null=False)
    surname = models.CharField(max_length=40, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        unique_together = (
            "name",
            "surname",
        )


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=60, blank=False, null=False)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    publication_date = models.DateField(blank=False, null=False)
    isbn = models.CharField(blank=False, null=False, max_length=13, unique=True)
    page_count = models.IntegerField()
    cover_photo = models.URLField(max_length=200)
    publication_language = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'"{self.title}" by {self.author}'
