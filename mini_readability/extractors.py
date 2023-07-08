# -*- coding: utf-8 -*-
import textwrap
from abc import ABC, abstractmethod
from dataclasses import dataclass
from bs4 import BeautifulSoup as Soup
from bs4 import Tag


@dataclass
class Article:
    title: str
    content: str = None
    datetime: str = None


class AbstractExtractor(ABC):

    @abstractmethod
    def check(self, url: str, document: Soup) -> bool:
        pass

    @abstractmethod
    def parse(self, document: Soup) -> tuple[Article]:
        pass

    @abstractmethod
    def format(self, articles: tuple[Article]) -> str:
        pass


class BaseExtractor(AbstractExtractor):

    def check(self, url: str, document: Soup):
        return True

    def parse(self, document: Soup):
        articles = []
        h1_candidates = document.findAll('h2')
        for h1 in h1_candidates:
            article = Article(h1.text)
            articles.append(article)

        return articles

    def format(self, articles: tuple[Article]) -> str:
        return "\n\n\n".join(map(lambda a: f"{a.title}\n\n{a.content}", articles))

    def _wrap(self, string):
        return "\n".join(textwrap.wrap(string, 80))

    def _process_links(self, element: Tag):
        links = element.select('a', href=True)
        for link in links:
            text = f"{link.text}[{link['href']}]"
            link.replaceWith(text)
        return element


def extract(url: str, document: Soup) -> str:
    import target_extractors
    for parser in BaseExtractor.__subclasses__():
        parser = parser()
        if parser.check(url, document):
            return parser.format(parser.parse(document))

    base_parser = BaseExtractor()
    return base_parser.format(base_parser.parse(document))
