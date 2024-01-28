def isbn10(isbn10: str) -> bool:
    if len(isbn10) != 10:
         return 0
    check_digit = sum([int(isbn10[i]) * (10 - i) if isbn10[i] != 'x' else 10 for i in range(10)]) % 11
    return not check_digit  # because 0 is correct

def isbn13(isbn13: str) -> bool:
    if len(isbn13) != 13:
        return 0
    check_digit = sum([int(isbn13[i]) * [1, 3][i % 2] for i in range(13)]) % 10
    return not check_digit  # because 0 is correct

def info_exist(dictionary, key):
    try:
        var = dictionary[key]
    except KeyError:
        var = ""
    return var