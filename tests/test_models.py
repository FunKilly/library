from django.test import TestCase

from books.models import Author, Book


class TestBookModel(TestCase):
    def test_add_author(self):
        book = Book.objects.create(
            title="one",
            publication_date="1970-01-01",
            isbn="12345x",
            page_count=100,
            cover_photo="www.google.pl",
            publication_language="pl",
        )
        author = "Jakub Grzedowicz"

        book.add_authors(author)

        author_exists = Author.objects.filter(name=author).exists()

        self.assertEqual(book.authors.first().name, author)
        self.assertTrue(author_exists)

    def test_add_multiple_authors(self):
        book = Book.objects.create(
            title="one",
            publication_date="1970-01-01",
            isbn="12345x",
            page_count=100,
            cover_photo="www.google.pl",
            publication_language="pl",
        )
        authors = "Dmitri Gluchovsky, Wojciech Cejrowski, H.P. Lovecraft"

        book.add_authors(authors)

        book_authors = [author.name for author in book.authors.all()]

        self.assertEqual(book_authors, authors.split(", "))
