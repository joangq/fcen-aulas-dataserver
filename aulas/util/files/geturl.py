from lxml import html
import requests
from requests import Response

from aulas.util.files.constants.mime import extensions
from aulas.util.files.inout import file
from aulas.util.strings import clean


def get_title(content: str):
    if isinstance(content, str):
        raise TypeError("Invalid content type " + str(type(content)))

    return html.fromstring(content).findtext(".//title")


def get_extension(filename: str, extension: str | None) -> str:
    fp: str
    dot_index: int
    if extension is None:
        dot_index = filename.rfind('.')
        if dot_index == -1:
            raise NameError("Can't save a file without extension.")
        fp = filename
    else:
        dot_index = extension.rfind('.')
        match dot_index:
            case -1:
                extension = '.' + extension
            case 0:
                pass
            case _:
                extension = extension[dot_index:]
        fp = filename + extension
    return fp


def save_str(content: str, path: str):
    with open(path, 'w') as f:
        f.write(content)


def save_bin(content: bytes, path: str):
    with open(path, 'wb') as f:
        f.write(content)


def save_as(content: str | bytes | object, filename: str, extension: str | None = None):
    fp = get_extension(filename, extension)
    match content:
        case str():
            return save_str(content, fp)
        case bytes():
            return save_bin(content, fp)
        case _:
            raise TypeError("Non supported type " + str(type(content)))


def geturl(url: str, filename: str | None = None, extension: str | None = None, path: str = './'):
    r: Response = requests.get(url)
    r.encoding = r.apparent_encoding

    mimetype: str
    mimetype = r.headers['Content-Type']
    mimetype = mimetype.split(';')[0]

    deduced_extension: str | None
    deduced_extension = extensions.get(mimetype)
    if deduced_extension in (".html", ".htm", ".shtml"):
        deduced_extension = '.html'

    filename_extension: str
    filename_extension = ''

    if filename is None:
        deduced_name: str
        deduced_name = ''

        if deduced_extension == '.html':
            deduced_name = get_title(r.text)
        else:
            try:
                deduced_name = r.headers['Content-Disposition']
                index = deduced_name.find('filename=')
                deduced_name = deduced_name[index + 9:]
                deduced_name = deduced_name.split(';')[0]
                deduced_name = deduced_name.replace('"', '').replace("'", "")
                index = deduced_name.rfind('.')
                deduced_name, filename_extension = deduced_name[:index], deduced_name[index:]
            except KeyError as e:
                print("Attribute " + str(e) + " not found while deducing name.")

        if filename is None:
            if deduced_name != '':
                filename = deduced_name
            else:
                raise NameError("Filename was not provided and couldn't be resolved automatically.")

    filename = clean(filename)
    #  filename = filename.replace(' ', '_')

    if extension is None:
        if filename_extension not in (None, ''):
            extension = filename_extension
        elif deduced_extension is not None:
            extension = deduced_extension
        else:
            raise TypeError("Extension was not provided and couldn't be resolved automatically.")

    return save_as(r.content, file(path + filename), extension)
