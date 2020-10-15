import requests
from django.conf import settings


def make_url_call(params):
    url = create_url(params)
    response = requests.get(url=url)
    response_json = response.json()

    return response_json


def create_url(params):
    url = "https://www.googleapis.com/books/v1/volumes?q="

    if params["general"]:
        url += params["general"]

    if params["isbn"]:
        url += f"+isbn:{params['isbn']}"

    for field in ["title", "author"]:
        if params[field]:
            url += f'+in{field}:"{params[field]}"'

    url += f"&key={settings.GOOGLE_API_KEY}"

    return url.replace(" ", "%")


def parse_response(response):
    book_records = []

    # Parser process only most accurate records, so we don't waste more memory
    for book in response["items"][:10]:
        record = book["volumeInfo"]

        # If the data lacks one of this crucial information, loop the loop goes to the next record
        if not all(
            [
                record.get("title"),
                record.get("publishedDate"),
                record.get("industryIdentifiers"),
            ]
        ):
            continue

        book_record = {
            "title": record["title"],
            "authors": ", ".join(record.get("authors", ["No info"])),
            "publication_date": record["publishedDate"],
            "publication_language": record.get("language", "No info"),
            "cover_photo_url": record.get("imageLinks"),
            "page_count": record.get("pageCount"),
        }

        # There are many types of ISBNs, the default and the newest one has 13 digits
        for number in record["industryIdentifiers"]:
            if number["type"] == ["ISBN_13"]:
                book_record["isbn"] = number["identifier"]
                break
            else:
                book_record["isbn"] = number["identifier"]

        # There are cases when the date includes only a year
        if len(book_record["publication_date"]) < 5:
            book_record["publication_date"] += "-01-01"

        if book_record["cover_photo_url"]:
            book_record["cover_photo_url"] = book_record["cover_photo_url"]["thumbnail"]

        book_records.append(book_record)

    return book_records
