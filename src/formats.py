def author(authors: list):
    return 0

def date(date: str):
    return 0

def name(title: str, subtitle: str) -> str:
    return f"\033[3m{': '.join([title, subtitle])}\033[0m"

def finalise(title, subtitle, name, date, authors):
    return f"{author(authors)}. {date(date)}. {name(title, subtitle)}"

#https://apastyle.apa.org/style-grammar-guidelines/references/examples/book-references