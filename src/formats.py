from datetime import datetime
import json
import os

import validate


# Constants
EXPORT_DIR = "./exports"
BOOK_EXPORT = os.path.join(EXPORT_DIR, "books.json")
WEBSITE_EXPORT = os.path.join(EXPORT_DIR, "websites.json")


class Book:
    def __init__(self, authors: list = [], title: str = "", subtitle: str = "", pdate: str = "", pub: str = "") -> None:
        self.authors = authors
        self.pdate = pdate
        self.title = title
        self.subtitle = subtitle
        self.pub = pub

    def author(self) -> str:
        all_authors = []
        for author in self.authors:
            author = author.split()

            # format each author
            name = author[-1]
            initials = ""
            for i in range(len(author) - 1):
                initials += f" {author[i][0]}."
            all_authors.append(f"{name},{initials}")

        # piece everything together
        ref = ""
        num_authors = len(all_authors)
        if num_authors == 1:
            ref = all_authors[0]
        else:
            for i in range(num_authors):
                if i == num_authors - 1:
                    ref += f"& {all_authors[i]}"
                else:
                    ref += f"{all_authors[i]}, "

        return ref

    def date(self) -> str:
        if self.pdate == "":
            return "(n.d.)"
        return f"({self.pdate.split("-")[0]})"

    def name(self) -> str:
        return f"\033[3m{': '.join([self.title, self.subtitle])}\033[0m"

    def publisher(self) -> str:
        # remove all words that indicate business purposes
        business_purposes = ["Inc.", "Incorporated", "Co.", "LLC"]
        pub = self.pub.split()
        for word in pub.copy():
            if word in business_purposes:
                pub.remove(word)
        pub = ' '.join(pub)

        # remove trailing punctuations
        if pub[-1] in ['.', ',']:
            pub = pub[:-1]

        return pub

    def finalise(self) -> str:
        author = self.author()
        date = self.date()
        name = self.name()
        publisher = self.publisher()
        return f"{author} {date}. {name}. {publisher}."

    def export_json(self) -> None:
        # Check if xport folder exist, if not then create
        if not os.path.exists(BOOK_EXPORT):
            os.makedirs(os.path.join(os.getcwd(), "exports"))
            with open(BOOK_EXPORT, 'x') as f:
                json.dump([], f)

        # Deserialisation
        data = {
                "title": self.title,
                "subtitle": self.subtitle,
                "authors": self.authors,
                "publishedDate": self.pdate,
                "publisher": self.pub
            }
        with open(BOOK_EXPORT, "r") as f:
            book_list = json.load(f)
        if data not in book_list:
            book_list.append(data)
        with open(BOOK_EXPORT, 'w') as f:
            json.dump(book_list, f, indent=4)

    def import_json(self) -> list:
        citations = []
        with open(BOOK_EXPORT, "r") as f:
            book_list = json.load(f)
        for book in book_list:
            self.authors = validate.info_exist(book, "authors")
            self.pdate = validate.info_exist(book, "publishedDate")
            self.title = validate.info_exist(book, "title")
            self.subtitle = validate.info_exist(book, "subtitle")
            self.pub = validate.info_exist(book, "publisher")

            citations.append(self.finalise())
        citations.sort()

        return citations


class Website:
    def __init__(self, authors: list = [], pdate: str = "", title: str = "", url: str = "") -> None:
        self.authors = authors
        self.pdate = pdate
        self.title = title
        self.url = url
        self.rdate = datetime.today().strftime("%B %d, %Y")

    def author(self) -> str:
        if not len(self.authors):
            return self.title

        all_authors = []
        for author in self.authors:
            author = author.split()

            # format each author
            name = author[-1]
            initials = ""
            for i in range(len(author) - 1):
                initials += f" {author[i][0]}."
            all_authors.append(f"{name},{initials}")

        # piece everything together
        ref = ""
        num_authors = len(all_authors)
        if num_authors == 1:
            ref = all_authors[0]
        else:
            for i in range(num_authors):
                if i == num_authors - 1:
                    ref += f"& {all_authors[i]}"
                else:
                    ref += f"{all_authors[i]}, "

        return ref

    def date(self) -> str:  # need check
        if self.pdate == "":
            return "(n.d.)"
        return f"({self.pdate.split("-")[0]})"

    def name(self) -> str:  # WIP
        pass

    def publisher(self) -> str:  # needs check
        # remove all words that indicate business purposes
        business_purposes = ["Inc.", "Incorporated", "Co.", "LLC"]
        pub = self.pub.split()
        for word in pub.copy():
            if word in business_purposes:
                pub.remove(word)
        pub = ' '.join(pub)

        # remove trailing punctuations
        if pub[-1] in ['.', ',']:
            pub = pub[:-1]

        return pub

    def retrieval(self):
        return f"Retrieved {self.rdate}, from {self.url}"

    def finalise(self) -> str:
        author = self.author()
        date = self.date()
        name = self.name()
        publisher = self.publisher()
        retrieval = self.retrieval()
        return f"{author} {date}. {name}. {publisher}. {retrieval}"
