# -*- coding: utf-8 -*-
import textwrap
from abc import ABC, abstractmethod
from dataclasses import dataclass
from bs4 import BeautifulSoup as Soup
from bs4 import Tag


def extract(url: str, document: Soup) -> str:
    for extractor in BaseExtractor.__subclasses__():
        extractor = extractor()
        if extractor.check(url, document):
            return extractor.format(extractor.parse(document))

    base_extractor = BaseExtractor()
    return base_extractor.format(base_extractor.parse(document))


@dataclass
class Article:
    title: str
    content: str = None
    datetime: str = None


class BaseExtractor:
    @abstractmethod
    def check(self, url: str, document: Soup) -> bool:
        return True

    @abstractmethod
    def parse(self, document: Soup) -> tuple[Article]:
        articles = []
        h1_candidates = document.findAll('h2')
        for h1 in h1_candidates:
            article = Article(h1.text)
            articles.append(article)

        return articles

    @abstractmethod
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


class LentaRuExtractor(BaseExtractor):

    def check(self, url: str, document: Soup):
        return "lenta.ru" in url

    def parse(self, document: Soup):
        title = document.findAll('span', class_='topic-body__title')
        date_time = document.findAll('a', class_='topic-header__time')
        content = document.findAll('div', class_='topic-body__content')
        article = Article(title[0].text)
        article.datetime = date_time[0].text
        article.content = self._wrap(self._process_links(content[0]).text)
        return (article,)

    def format(self, articles: tuple[Article]) -> str:
        return "\n\n\n".join(map(lambda a: f"{a.datetime}\n{a.title}\n\n{a.content}", articles))


class GoogleSearchExtractor(BaseExtractor):

    def check(self, url: str, document: Soup):
        return "google.com/search?q=" in url

    def parse(self, document: Soup):
        links = document.select("a:has(h3)", href=True)
        articles = []
        for link in links:
            title = link.find('h3').text
            href = link['href']
            articles.append(Article(self._wrap(f"{title} [{href}]")))
        return tuple(articles)

    def format(self, articles: tuple[Article]) -> str:
        return "\n\n\n".join(map(lambda a: f"{a.title}", articles))
