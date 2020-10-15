from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    authors = forms.CharField(
        help_text="Enter authors if u want to change it. Separate multiple authors with a comma.",
        required=False,
    )
    publication_date = forms.DateField(
        input_formats=["%Y-%m-%d"], help_text="Input format: YYYY-MM-DD"
    )

    class Meta:
        model = Book
        fields = [
            "title",
            "publication_date",
            "publication_language",
            "isbn",
            "page_count",
            "cover_photo",
        ]
