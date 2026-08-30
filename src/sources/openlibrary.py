import requests

from .base import BaseScraper


class OpenLibraryScraper(BaseScraper):

    def __init__(self, query, limit=10):
        self.query = query
        self.limit = limit

    def extract(self):
        response = requests.get(
            "https://openlibrary.org/search.json",
            params={
                "q": self.query,
                "limit": self.limit
            },
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    def transform(self, data):
        books = []

        for book in data.get("docs", []):
            title = book.get("title", "Unknown")

            authors = book.get("author_name", ["Unknown"])
            author = ", ".join(authors[:2])

            year = book.get("first_publish_year")

            books.append({
                "title": title,
                "author": author,
                "year": year
            })

        return books
