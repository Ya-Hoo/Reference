import urllib.request, json

API_LINK = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
BOOKS = "sources/books.txt"
WEBSITES = "sources/websites.txt"

def validate_isbn10(isbn10: str) -> bool:
    return 0

def validate_isbn13(isbn13: str) -> bool:
    return 0

with open(BOOKS, 'r') as f:
    for isbn in f:
        if validate_isbn10(isbn) or validate_isbn13(isbn):
            with urllib.request.urlopen(API_LINK + isbn) as book:
                data = book.read()
                