def author(name: list):
    return 0

def date(date: str):
    return 0

def name(title: str, subtitle: str) -> str:
    return f"\033[3m{': '.join([title, subtitle])}\033[0m"
