from unidecode import unidecode  # https://github.com/avian2/unidecode/


def clean(x: str) -> str:
    return unidecode(x).replace(' ', '-').lower()