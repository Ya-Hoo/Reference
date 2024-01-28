from urllib.request import urlopen
import json


class Book:
    def __init__(self, isbn) -> None:        
        API_LINK = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
        INFO_LINK = "https://www.googleapis.com/books/v1/volumes/"
        with urlopen(API_LINK + isbn) as request:
            BOOK_ID = json.loads(request.read())["items"][0]["id"]
        
        # Getting all necessary info and put as dictionary
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
    def __init__(self) -> None:
        pass
    # https://github.com/thenaterhood/python-autocite/blob/master/src/python_autocite/lib/datafinder.py