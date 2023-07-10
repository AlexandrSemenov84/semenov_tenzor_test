# -*- coding: utf-8 -*-
import sys
from functools import reduce
from bs4 import BeautifulSoup as Soup
import requests
from pathlib import Path
from urllib.parse import urlparse
from requests.exceptions import InvalidURL, MissingSchema
from extractors import extract


def print_to_file(url_str: str, text: str) -> str:
    url = urlparse(url_str)
    path = url.path
    if path.endswith("/"):
        path = path[:-1]

    if not path:
        file_name = 'index.txt'
    else:
        page_extensions = ('.html', '.htm', '.php', '.php3', '.phtml', '.shtml')
        is_page = reduce(lambda acc, ext: acc or path.endswith(ext), page_extensions, False)
        if is_page:
            path = path[:path.rindex('.')]

        file_name = path[path.rindex('/') + 1:]

    file_extension = '.txt'
    dir_name = "output/" + url.netloc + path[:len(path) - len(file_name)]
    Path(dir_name).mkdir(parents=True, exist_ok=True)

    file_path = dir_name + file_name + file_extension
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

    return file_path


def main():
    if len(sys.argv) == 1:
        print("Необходимо передать параметр — url ресурса.")
        return

    url_str = sys.argv[1]

    try:
        response = requests.get(url_str)
    except (InvalidURL, MissingSchema) as error:
        print(f"Некорректный url: {error}")
        return
    if response.status_code != 200:
        print(f"Не удалось загрузить ресурс по укзанному адресу. Код ошибки: {response.status_code}")
        return
    document = Soup(response.text, "html.parser")
    text = extract(url_str, document)
    file_path = print_to_file(url_str, text)
    print(f"Результат записан в файл: {file_path}")


if __name__ == '__main__':
    main()
