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


def decor(msg: str, code: int) -> None:
    if " >> " in msg:
        pre_msg, post_msg = msg.split(" >> ")
    match code:
        case 0:  # alert
            print(f"{pre_msg} >>\033[1;31m {post_msg} \033[0m")
        case 1:  # success
            print(f"{pre_msg} >>\033[1;32m {post_msg} \033[0m")
        case 2:  # warning
            print(f"\n\033[1;33m{msg}\033[0m")
        case 3:  # process status/headers
            print(f"\n\033[1;34m{msg.upper()}\033[0m")


decor("======================== Retrieving data ========================", 3)
print(f"File \"{BOOKS.split('\\')[-1]}\"")
with open(BOOKS, 'r') as f:
    for index, isbn in enumerate(f):
        isbn = isbn.rstrip()
        if validate.isbn10(isbn) or validate.isbn13(isbn):
            with urllib.request.urlopen(API_LINK + isbn) as request:
                decor(f"    - Line {index + 1} >> SUCCESS", 1)
              
                BOOK_ID = json.loads(request.read())["items"][0]["id"]
            
            # Getting all necessary info and put as dictionary
            with urllib.request.urlopen(INFO_LINK + BOOK_ID) as book:
                book_data = json.loads(book.read())
                vol_info = book_data['volumeInfo']

            # Extracting data
            TITLE = validate.info_exist(vol_info, "title")
            SUBTITLE = validate.info_exist(vol_info, "subtitle")
            AUTHORS = validate.info_exist(vol_info, "authors")
            DATE = validate.info_exist(vol_info, "publishedDate")
            PUBLISHER = validate.info_exist(vol_info, "publisher")
            BookInfo = formats.Books(authors=AUTHORS, title=TITLE, subtitle=SUBTITLE, pdate=DATE, pub=PUBLISHER)
            
            # Formatting into APA
            CITATIONS.append(BookInfo.finalise())
            
            # Exporting json reference
            BookInfo.export_json()
            
        else:
            decor(f"    - Line {index + 1} >> ERROR: Invalid ISBN", 0)

decor("========================= bibliography ==========================", 3)
CITATIONS.sort()
for i in CITATIONS:
    print(i)
    
decor("=========================== editing =============================", 3)
change = input("Do you want to change any citation details (y/n): ").lower()
if change == 'y':
    decor("WARNING: Before you type 1, please remember to save the json file.", 2)
    proceed = int(input("When you finished editing books.json, type 1: "))
    CITATIONS = formats.Books().import_json()
    
    decor("====================== final bibliography =======================", 3)
    for i in CITATIONS:
        print(i)
        
    
