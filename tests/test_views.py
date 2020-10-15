from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from books.models import Author, Book


class TestHomePageView(TestCase):
    def test_get(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


class TestBookListView(TestCase):
    def setUp(self):
        books = Book.objects.bulk_create(
            [
                Book(
                    title="one",
                    publication_date="1970-01-01",
                    isbn="12345x",
                    page_count=100,
                    cover_photo="www.google.pl",
                    publication_language="pl",
                ),
                Book(
                    title="two",
                    publication_date="1980-01-01",
                    isbn="12346x",
                    page_count=100,
                    cover_photo="www.google.pl",
                    publication_language="pl",
                ),
                Book(
                    title="three",
                    publication_date="1990-01-01",
                    isbn="12347x",
                    page_count=100,
                    cover_photo="www.google.pl",
                    publication_language="pl",
                ),
            ]
        )
        authors = Author.objects.bulk_create(
            [
                Author(name="Stephen King"),
                Author(name="Andriej Diakow"),
                Author(name="Dan Simmons"),
            ]
        )
        for author, book in zip(authors, books):
            book.authors.add(author)

    def test_get(self):
        response = self.client.get(reverse("book_list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data["context"]), 3)

    def test_filtered_get(self):
        response = self.client.get("/books/?publication_date_min=1975-01-01")
        self.assertEqual(len(response.context_data["context"]), 2)

        response = self.client.get("/books/?title__icontains=one")
        self.assertEqual(len(response.context_data["context"]), 1)

        response = self.client.get("/books/?authors=Stephen")
        self.assertEqual(len(response.context_data["context"]), 1)


class TestBookCreateView(TestCase):
    def test_get(self):
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        data = {
            "title": "one",
            "publication_date": "1970-01-01",
            "isbn": "12345x",
            "page_count": 100,
            "cover_photo": "https://www.google.pl",
            "publication_language": "pl",
            "authors": "Brandon Sanderson",
        }
        response = self.client.post(reverse("book_create"), data=data)

        book = Book.objects.filter(isbn=data["isbn"]).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            [
                book.title,
                str(book.publication_date),
                book.publication_language,
                book.page_count,
                book.cover_photo,
            ],
            [
                data["title"],
                data["publication_date"],
                data["publication_language"],
                data["page_count"],
                data["cover_photo"],
            ],
        )
        self.assertEqual(
            book.authors.filter(name=data["authors"]).first().name, data["authors"]
        )


class TestBookUpdateView(TestCase):
    def test_post(self):
        book = Book.objects.create(
            title="one",
            publication_date="1970-01-01",
            isbn="12345x",
            page_count=100,
            cover_photo="https://www.google.pl",
            publication_language="pl",
        )
        author = Author.objects.create(name="John Cena")
        book.authors.add(author)

        data = {
            "title": "two",
            "page_count": 200,
            "publication_date": "1970-01-01",
            "isbn": "12345x",
            "publication_language": "pl",
            "cover_photo": "https://www.google.pl",
            "authors": "John Cena, Johnson's Baby",
        }
        response = self.client.post(
            reverse("book_update", kwargs={"pk": book.pk}), data=data
        )

        book.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            [data["title"], data["page_count"]], [book.title, book.page_count]
        )
        self.assertEqual(
            data["authors"].split(", "), [author.name for author in book.authors.all()]
        )


class TestBookDeleteView(TestCase):
    def test_post(self):
        book = Book.objects.create(
            title="one",
            publication_date="1970-01-01",
            isbn="12345x",
            page_count=100,
            cover_photo="https://www.google.pl",
            publication_language="pl",
        )
        author = Author.objects.create(name="John Cena")
        book.authors.add(author)

        response = self.client.post(reverse("book_delete", kwargs={"pk": book.pk}))

        book_exists = Book.objects.filter(id=book.id).exists()
        author_exists = Author.objects.filter(id=author.id).exists()

        self.assertEqual(response.status_code, 302)
        self.assertFalse(book_exists)
        self.assertTrue(author_exists)


class TestBookSearchView(TestCase):
    def test_get(self):
        response = self.client.get(reverse("book_search"))
        self.assertEqual(response.status_code, 200)

    @patch(
        "books.views.BookSearchView.get_books",
        return_value=[
            ("title", "Ges i osiol"),
            ("authors", "Julian Ursyn Niemcewicz"),
            ("isbn", "9788303012647"),
            ("publication_language", "en"),
            ("publication_date", "1986-01-01"),
            ("cover_photo_url", ""),
            ("page_count", 12),
        ],
    )
    def test_post(self, mock):
        data = {"title": "Osiol"}
        response = self.client.post(reverse("book_search"), data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["data"], mock.return_value)

    @patch("books.views.BookSearchView.get_books", return_value=[])
    def test_post_no_results(self, mock):
        data = {"title": "Osiol"}
        response = self.client.post(reverse("book_search"), data)

        self.assertEqual(response.status_code, 200)


class TestBookSearchResultsImportView(TestCase):
    @patch(
        "django.core.cache.cache.get",
        return_value={
            "title": "Ges i osiol",
            "authors": "Julian Ursyn Niemcewicz",
            "publication_language": "en",
            "publication_date": "1986-01-01",
            "cover_photo_url": "",
            "page_count": 12,
        },
    )
    def test_get(self, mock):
        isbn = "9788303012647"
        response = self.client.get(
            reverse("book_search_results_import", kwargs={"isbn": isbn})
        )

        book = Book.objects.filter(isbn=isbn).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            [
                book.title,
                str(book.publication_date),
                book.publication_language,
                book.page_count,
                book.cover_photo,
                book.authors.first().name,
            ],
            [
                mock.return_value["title"],
                mock.return_value["publication_date"],
                mock.return_value["publication_language"],
                mock.return_value["page_count"],
                mock.return_value["cover_photo_url"],
                mock.return_value["authors"],
            ],
        )

    @patch(
        "django.core.cache.cache.get", return_value=None,
    )
    def test_get_with_cache_expired(self, mock):
        isbn = "9788303012647"
        response = self.client.get(
            reverse("book_search_results_import", kwargs={"isbn": isbn})
        )

        book_exists = Book.objects.filter(isbn=isbn).exists()

        self.assertEqual(response.status_code, 302)
        self.assertFalse(book_exists)


class TestRESTBookListView(TestCase):
    def setUp(self):
        books = Book.objects.bulk_create(
            [
                Book(
                    title="one",
                    publication_date="1970-01-01",
                    isbn="12345x",
                    page_count=100,
                    cover_photo="www.google.pl",
                    publication_language="pl",
                ),
                Book(
                    title="two",
                    publication_date="1980-01-01",
                    isbn="12346x",
                    page_count=100,
                    cover_photo="www.google.pl",
                    publication_language="pl",
                ),
                Book(
                    title="three",
                    publication_date="1990-01-01",
                    isbn="12347x",
                    page_count=100,
                    cover_photo="www.google.pl",
                    publication_language="pl",
                ),
            ]
        )
        authors = Author.objects.bulk_create(
            [
                Author(name="Stephen King"),
                Author(name="Andriej Diakow"),
                Author(name="Dan Simmons"),
            ]
        )
        for author, book in zip(authors, books):
            book.authors.add(author)

    def test_get(self):
        response = self.client.get(reverse("book_list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data["context"]), 3)

    def test_filtered_get(self):
        response = self.client.get("/books/?publication_date_min=1975-01-01")
        self.assertEqual(len(response.context_data["context"]), 2)

        response = self.client.get("/books/?title__icontains=one")
        self.assertEqual(len(response.context_data["context"]), 1)

        response = self.client.get("/books/?authors=Stephen")
        self.assertEqual(len(response.context_data["context"]), 1)
