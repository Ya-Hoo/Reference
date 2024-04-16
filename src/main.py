import os

import datafinder
import validate
import formats


# Constants
REFERENCES = "./references"
BOOKS = os.path.join(REFERENCES, "books.txt")
WEBSITES = os.path.join(REFERENCES, "websites.txt")
CITATIONS = []


# just decorating print stuff with colours
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


# Check if reference folder exist, if not then create
if not os.path.exists(REFERENCES):
    os.makedirs(os.path.join(os.getcwd(), "references"))
    with open(BOOKS, 'x') as f:
        pass
    with open(WEBSITES, 'x') as f:
        pass
    exit()


decor("======================== Retrieving data ========================", 3)
print(f"File \"{BOOKS.split('\\')[-1]}\"")
with open(BOOKS, 'r') as f:
    for index, isbn in enumerate(f):
        isbn = isbn.rstrip()
        if validate.isbn10(isbn) or validate.isbn13(isbn):

            # Extracting data
            book = datafinder.Book(isbn)
            if not book.found:
                decor(f"    - Line {index + 1} >> ERROR: Book Not Found", 0)
                continue

            decor(f"    - Line {index + 1} >> SUCCESS", 1)
            _, TITLE, SUBTITLE, AUTHORS, DATE, PUBLISHER = book.__dict__.values()
            BookInfo = formats.Book(AUTHORS, TITLE, SUBTITLE, DATE, PUBLISHER)

            # Formatting into APA
            CITATIONS.append(BookInfo.finalise())

            # Exporting json reference
            BookInfo.export_json()

        else:
            decor(f"    - Line {index + 1} >> ERROR: Invalid ISBN", 0)


print(f"File \"{WEBSITES.split('\\')[-1]}\"")
with open(WEBSITES, 'r') as f:
    for index, url in enumerate(f):
        url = url.rstrip()
        if validate.url(url):
            decor(f"    - Line {index + 1} >> SUCCESS", 1)

            # Extracting data
            datafinder.Website(url)

        else:
            decor(f"    - Line {index + 1} >> ERROR: Invalid URL", 0)


decor("========================= bibliography ==========================", 3)
CITATIONS.sort()
for i in CITATIONS:
    print(i)

decor("=========================== editing =============================", 3)
change = input("Do you want to change any citation details (y/n): ").lower()
if change == 'y':
    decor("WARNING: Before you type 1, please save the json file.", 2)
    proceed = int(input("When you finished editing books.json, type 1: "))
    CITATIONS = formats.Books().import_json()

decor("====================== final bibliography =======================", 3)
for i in CITATIONS:
    print(i)

decor("WARNING: When copying the text from terminal into a Doc, the italics"
      "will disappear. Just remember to reformat it afterwards.", 2)
