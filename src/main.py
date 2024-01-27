import urllib.request, json

import validate
import formats

API_LINK = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
BOOKS = "./references/books.txt"
WEBSITES = "./references/websites.txt"

def txt_decor(msg: str, code: int) -> None:
    match code:
        case 0:  # alert
            print(f"\033[1;31m {msg} \033[0m")
        case 1:  # success
            print(f"\033[1;32m {msg} \033[0m")
        case 2:  # warning
            print(f"\033[1;33m {msg} \033[0m")

with open(BOOKS, 'r') as f:
    print(f"File \"{BOOKS.split('/')[-1]}\"")
    for index, isbn in enumerate(f):
        isbn = isbn.rstrip()
        if validate.isbn10(isbn) or validate.isbn13(isbn):
            with urllib.request.urlopen(API_LINK + isbn) as book:
                msg = f"Line {index + 1} >> SUCCESS"
                txt_decor(msg, 1)
                data = json.loads(book.read())
                
                vol_info = data["volumeInfo"]
                TITLE, SUBTITLE = vol_info["title"], vol_info["subtitle"]
                AUTHORS, DATE = vol_info["authors"], vol_info["publishedDate"]
        else:
            msg = f"Line {index + 1} >> ERROR: Invalid ISBN\n"
            txt_decor(msg, 0)
            