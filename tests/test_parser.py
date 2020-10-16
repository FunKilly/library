from unittest.mock import patch

from django.test import TestCase

from books.integrations import google_api


class TestGoogleApiIntegration(TestCase):
    @patch("django.conf.settings.GOOGLE_API_KEY", "123")
    def test_create_url(self):
        params = {"general": "fog", "title": "this", "author": "", "isbn": ""}
        url = 'https://www.googleapis.com/books/v1/volumes?q=fog+intitle:"this"&key=123'

        api_url = google_api.create_url(params)

        self.assertEqual(api_url, url)

    def test_parse_response(self):
        title = "numero"
        authors = ["Albi Libellud"]
        publication_date = "1970-01-01"
        publication_language = "esp"
        cover_photo_url = "https://www.nasza-klasa.pl"
        isbn = "19700101"
        page_count = 404

        volumeInfo = {
            "title": title,
            "authors": authors,
            "publishedDate": publication_date,
            "language": publication_language,
            "Paolo": "Coehlo",
            "imageLinks": {"thumbnail": cover_photo_url},
            "pageCount": page_count,
            "industryIdentifiers": [
                {"identifier": "12345", "type": "ISBN_10"},
                {"identifier": isbn, "type": "ISBN_13"},
            ],
            "dusty": "dust",
        }

        response = {"items": [{"volumeInfo": volumeInfo}]}
        parsed_response = google_api.parse_response(response)[0]

        self.assertEqual(
            [
                title,
                ", ".join(authors),
                publication_date,
                publication_language,
                cover_photo_url,
                page_count,
                isbn,
            ],
            [
                parsed_response["title"],
                parsed_response["authors"],
                parsed_response["publication_date"],
                parsed_response["publication_language"],
                parsed_response["cover_photo_url"],
                parsed_response["page_count"],
                parsed_response["isbn"],
            ],
        )
