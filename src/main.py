import urllib.request, json, os

import validate
import formats

API_LINK = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
REFERENCES = "./references"
BOOKS = os.path.join(REFERENCES, "books.txt")
WEBSITES = os.path.join(REFERENCES, "websites.txt")
CITATIONS = []


def txt_decor(msg: str, code: int) -> None:
    match code:
        case 0:  # alert
            print(f"\033[1;31m {msg} \033[0m")
        case 1:  # success
            print(f"\033[1;32m {msg} \033[0m")
        case 2:  # warning
            print(f"\033[1;33m {msg} \033[0m")


if not os.path.exists(REFERENCES):
    os.makedirs(os.path.join(os.getcwd(), "references"))
    with open(BOOKS, 'x') as f: pass
    with open(WEBSITES, 'x') as f: pass
    
def check_info_exist(dictionary, key):
    try:
        var = dictionary[key]
    except KeyError:
        var = None
    return var

with open(BOOKS, 'r') as f:
    print(f"File \"{BOOKS.split('/')[-1]}\"")
    for index, isbn in enumerate(f):
        isbn = isbn.rstrip()
        if validate.isbn10(isbn) or validate.isbn13(isbn):
            with urllib.request.urlopen(API_LINK + isbn) as book:
                msg = f"Line {index + 1} >> SUCCESS"
                txt_decor(msg, 1)
                
                # Book data extraction
                data = json.loads(book.read())
                vol_info = data["items"][0]["volumeInfo"]
                TITLE = check_info_exist(vol_info, "title")
                SUBTITLE = check_info_exist(vol_info, "subtitle")
                AUTHORS = check_info_exist(vol_info, "authors")
                DATE = check_info_exist(vol_info, "publishedDate")
                
                print(TITLE, SUBTITLE, AUTHORS, DATE)
                
                # Formatting into APA
                BookInfo = formats.Books(authors=AUTHORS, title=TITLE, subtitle=SUBTITLE, date=DATE)
                CITATIONS.append(BookInfo.finalise())
        else:
            msg = f"Line {index + 1} >> ERROR: Invalid ISBN\n"
            txt_decor(msg, 0)
            