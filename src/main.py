import urllib.request, json, os

import validate
import formats


# Constants
API_LINK = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
INFO_LINK = "https://www.googleapis.com/books/v1/volumes/"
REFERENCES = "./references"
BOOKS = os.path.join(REFERENCES, "books.txt")
WEBSITES = os.path.join(REFERENCES, "websites.txt")
CITATIONS = []

# Check if reference folder exist, if not then create
if not os.path.exists(REFERENCES):
    os.makedirs(os.path.join(os.getcwd(), "references"))
    with open(BOOKS, 'x') as f: pass
    with open(WEBSITES, 'x') as f: pass
    exit()


def txt_decor(msg: str, code: int) -> None:
    pre_msg, post_msg = msg.split(" >> ")
    match code:
        case 0:  # alert
            print(f"{pre_msg} >>\033[1;31m {post_msg} \033[0m")
        case 1:  # success
            print(f"{pre_msg} >>\033[1;32m {post_msg} \033[0m")
        case 2:  # warning
            print(f"{pre_msg} >>\033[1;33m {post_msg} \033[0m")
        case 3:  # process status
            print(f"{pre_msg} >>\033[1;33m {post_msg} \033[0m")


def check_info_exist(dictionary, key):
    try:
        var = dictionary[key]
    except KeyError:
        var = None
    return var


with open(BOOKS, 'r') as f:
    print(f"File \"{BOOKS.split('\\')[-1]}\"")
    for index, isbn in enumerate(f):
        isbn = isbn.rstrip()
        if validate.isbn10(isbn) or validate.isbn13(isbn):
            with urllib.request.urlopen(API_LINK + isbn) as request:
                msg = f"Line {index + 1} >> SUCCESS"
                txt_decor(msg, 1)
                
                # Getting ID
                request_data = json.loads(request.read())                
                BOOK_ID = request_data["items"][0]["id"]
            
            # Getting all necessary info and put as dictionary
            with urllib.request.urlopen(INFO_LINK + BOOK_ID) as book:
                book_data = json.loads(book.read())
                vol_info = book_data['volumeInfo']

            # Extracting data
            TITLE = check_info_exist(vol_info, "title")
            SUBTITLE = check_info_exist(vol_info, "subtitle")
            AUTHORS = check_info_exist(vol_info, "authors")
            DATE = check_info_exist(vol_info, "publishedDate")
            PUBLISHER = check_info_exist(vol_info, "publisher")
            
            # Formatting into APA
            BookInfo = formats.Books(authors=AUTHORS, title=TITLE, subtitle=SUBTITLE, pdate=DATE, pub=PUBLISHER)
            CITATIONS.append(BookInfo.finalise())
            
        else:
            msg = f"Line {index + 1} >> ERROR: Invalid ISBN\n"
            txt_decor(msg, 0)




CITATIONS.sort()
for i in CITATIONS:
    print(i)