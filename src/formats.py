class Books:
    def __init__(self, authors, title, subtitle, date, publisher) -> None:
        self.authors = authors
        self.date = date
        self.title = title
        self.subtitle = subtitle
        self.publisher = publisher
        
        
    def author(self) -> str:
        all_authors = []
        for author in self.authors:
            author = author.split(" ")
            
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
        if self.date == "":
            return f"(n.d.)"
        return f"({self.date.split("-")[0]})"


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