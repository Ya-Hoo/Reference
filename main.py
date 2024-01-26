import urllib.request, json

API_LINK = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
BOOKS = "sources/books.txt"
WEBSITES = "sources/websites.txt"

def validate_isbn10(isbn10: str) -> bool:
    if len(isbn10) != 10:
         return 0
    check_digit = sum([int(isbn10[i]) * (10 - i) if isbn10[i] != 'x' else 10 for i in range(10)]) % 11
    return not check_digit  # because 0 is correct

def validate_isbn13(isbn13: str) -> bool:
    if len(isbn13) != 13:
        return 0
    check_digit = sum([int(isbn13[i]) * [1, 3][i % 2] for i in range(13)]) % 10
    return not check_digit  # because 0 is correct

def txt_decor(msg: str, code: int):
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
        if validate_isbn10(isbn) or validate_isbn13(isbn):
            with urllib.request.urlopen(API_LINK + isbn) as book:
                msg = f"Line {index + 1} >> SUCCESS"
                txt_decor(msg, 1)
                data = book.read()
        else:
            msg = f"Line {index + 1} >> ERROR: Invalid ISBN\n"
            txt_decor(msg, 0)
            