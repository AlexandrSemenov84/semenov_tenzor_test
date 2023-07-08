import unittest

import requests
from bs4 import BeautifulSoup as Soup

from mini_readability.extractors import LentaRuExtractor


class TargetExtractorsTest(unittest.TestCase):
    def test_lenta_ru_parser(self):
        url_str = 'https://lenta.ru/news/2023/07/05/akkurat_akkurat/'
        response = requests.get(url_str)
        document = Soup(response.text, "html.parser")
        articles = LentaRuExtractor().parse(document)
        self.assertTrue(len(articles) == 1, "Не удалось получить статью")
        self.assertEqual(articles[0].title, "Путин рассказал об обстановке в новых регионах России")
        self.assertTrue(articles[0].content.startswith("В настоящее время в новых регионах России[/tags/geo/rf/]"))


if __name__ == '__main__':
    unittest.main()
