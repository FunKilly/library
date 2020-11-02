import uuid

from django.db import models


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} "


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, blank=False, null=False)
    publication_date = models.DateField(blank=False, null=False)
    isbn = models.CharField(max_length=20, unique=True)
    page_count = models.IntegerField(null=True, blank=True)
    cover_photo = models.URLField(max_length=200, null=True, blank=True)
    publication_language = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    authors = models.ManyToManyField(Author, through="BookAuthor")

    def __str__(self):
        authors_list = [author.name for author in self.authors.all()]
        return f'"{self.title}" by {", ".join(authors_list)}'

    def add_authors(self, authors):
        if authors in [None, ""]:
            unknown_author, _ = Author.objects.get_or_create(name="Unknown")
            self.authors.add(unknown_author)
        else:
            author_objects = []
            authors = self.extract_authors(authors)
            for author in authors:
                author_object = Author.objects.filter(name=author).first()
                if author_object:
                    author_objects.append(author_object)
                else:
                    author_object = Author.objects.create(name=author)
                    author_objects.append(author_object)

            self.authors.set(author_objects)

    @staticmethod
    def extract_authors(authors):
        authors = [author.rstrip().lstrip() for author in authors.split(",")]
        return authors


class BookAuthor(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="bookauthors_set",
    )
    news = models.ForeignKey(Author, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
