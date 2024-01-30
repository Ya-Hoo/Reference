from urllib.request import urlopen
import json


class Book:
    def __init__(self, isbn) -> None:
        API_LINK = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
        INFO_LINK = "https://www.googleapis.com/books/v1/volumes/"
        self.found = False

        self.title = ""
        self.subtitle = ""
        self.authors = ""
        self.date = ""
        self.publisher = ""

        with urlopen(API_LINK + isbn) as request:
            try:
                BOOK_ID = json.loads(request.read())["items"][0]["id"]
                self.found = True
            except KeyError:
                pass

        # Getting all necessary info and put as dictionary
        if self.found:
            with urlopen(INFO_LINK + BOOK_ID) as book:
                book_data = json.loads(book.read())
                vol_info = book_data['volumeInfo']

            # Extracting data
            self.title = self.get_data(vol_info, "title")
            self.subtitle = self.get_data(vol_info, "subtitle")
            self.authors = self.get_data(vol_info, "authors")
            self.date = self.get_data(vol_info, "publishedDate")
            self.publisher = self.get_data(vol_info, "publisher")

    def get_data(self, dictionary: dict, key: str):
        try:
            var = dictionary[key]
        except KeyError:
            var = ""
        return var


class Website:
    def __init__(self, soup) -> None:
        self.soup = soup

    def get_author(self):
        authors = set()
        searches = [
            {'name': 'author'},
            {'property': 'article:author'},
            {'property': 'author'},
            {'rel': 'author'}
        ]

        author_elements = []
        for s in searches:
            author_elements += self.soup.find_all(attrs=s)

        for el in author_elements:
            author = self.get_data_from_element(el)
            if (len(author.split()) > 1):
                authors.add(author)

        authors_list = list(authors)
        return authors_list

    def get_title(self):
        pass
    # https://github.com/thenaterhood/python-autocite/blob/master/src/python_autocite/lib/datafinder.py
