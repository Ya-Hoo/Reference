class Books:
    def __init__(self, authors, title, subtitle="", date="n.d") -> None:
        self.authors = authors
        self.date = date
        self.title = title
        self.subtitle = subtitle
        
    def author(self) -> str:
        for author in self.authors:
            author = author.split()[::-1]
            name = author[0]
            initials = author[-1][0]
        return 0

    def date(self) -> str:
        return 0

    def name(self) -> str:
        return f"\033[3m{': '.join([self.title, self.subtitle])}\033[0m"

    def finalise(self) -> str:
        return f""
    
    def export_json(self) -> None:
        return
    
    def export_txt(self) -> None:
        return
        
    def import_json(self) -> None:
        return
#https://apastyle.apa.org/style-grammar-guidelines/references/examples/book-references