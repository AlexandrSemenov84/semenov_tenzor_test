# -*- coding: utf-8 -*-
import string
import textwrap
from abc import ABC, abstractmethod
from dataclasses import dataclass
from bs4 import BeautifulSoup as Soup
from bs4 import Tag
from urllib.parse import unquote
from functools import reduce
from string import Template


def extract(url: str, document: Soup) -> str:
    for extractor_class in AbstractExtractor.__subclasses__():
        extractor = extractor_class()
        if extractor.check(url, document):
            return extractor.format(extractor.parse(document))

    default_extractor = DefaultExtractor()
    return default_extractor.format(default_extractor.parse(document))


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


class DefaultExtractor(AbstractExtractor):

    def check(self, url: str, document: Soup) -> bool:
        return False

    def parse(self, document: Soup) -> tuple[Article]:
        # убираем ненужное
        should_be_excluded = []
        should_be_excluded.append(document.findAll(('header', 'nav', 'footer', 'sup')))
        should_be_excluded.append(document.findAll(None, {'aria-hidden': 'true'}))
        should_be_excluded.append(document.findAll(None, style=lambda value: value and 'display:none' in value))
        for result_set in should_be_excluded:
            for tag in result_set:
                tag.extract()

        # Если в списке только ссылки - удаляем
        should_be_excluded = document.findAll(('ul', 'ol'))
        for tag in should_be_excluded:
            items = tag.select('li')
            is_tags_list = reduce(lambda acc, item: acc or len(item.contents) == 1 and item.contents[0].name == 'a',
                                  items, False)
            if is_tags_list:
                tag.extract()

        # ToDo Научиться обрабатывать таблицы. Пока просто вырезаем их.
        tables = document.findAll('table')
        for table in tables:
            table.extract()

        # Извлекаем полезное
        elements = document.findAll(('h1', 'h2', 'h3', 'p', 'ul', 'ol', 'pre'))
        elements.sort(key=lambda e: e.sourceline)
        articles = []
        article = None
        paragraphs = []
        for tag in elements:
            if tag.hidden:
                continue
            if tag.name == 'h1' or tag.name == 'h2' or tag.name == 'h3':
                # Если есть статья, сохраняем её и создаем новую
                if article is not None and bool(paragraphs):
                    article.content = "\n\n".join(paragraphs)
                    paragraphs = []
                    articles.append(article)
                h_links = tag.find_all('a')
                for h_link in h_links:
                    h_link.extract()
                h_contents = tag.contents
                for h_content in h_contents:
                    if len(h_content.text) < 6:
                        h_content.extract()
                article = Article(tag.text)
                continue
            if tag.name == 'pre':
                paragraphs.append(f"```\n{Utils.wrap(tag.text)}\n```")
                continue
            if tag.name == 'ul':
                items = tag.select('li')
                items = map(lambda i: Utils.wrap("• " + Utils.process_links(i).text), items)
                paragraphs.append("\n".join(items))
                continue
            if tag.name == 'ol':
                items = tag.select('li')
                items = [Utils.wrap(str(index) + '. ' + Utils.process_links(item).text) for index, item in
                         enumerate(items, start=1)]
                paragraphs.append("\n".join(items))
                continue
            paragraphs.append(Utils.wrap(Utils.process_links(tag).text))

        if article is not None and bool(paragraphs):
            article.content = "\n\n".join(paragraphs)
            articles.append(article)

        return articles

    def format(self, articles: tuple[Article]) -> str:
        if not articles:
            return "К сожалению, ничего не нашлось."
        with open('template.txt', 'r') as file:
            template_str = file.read()
        if template_str:
            template = string.Template(template_str)
            if template.is_valid():

                def mapper(article):
                    title = article.title
                    content = article.content
                    datetime = article.datetime
                    return template.safe_substitute(locals())

                return "".join(map(mapper, articles))
            else:
                raise ValueError("Неверный формат шаблона")

        return "\n\n\n".join(map(lambda a: f"{Utils.wrap('  ' + a.title)}\n\n{a.content}", articles))


class LentaRuExtractor(AbstractExtractor):

    def check(self, url: str, document: Soup):
        return "lenta.ru" in url

    def parse(self, document: Soup):
        title = document.findAll('span', class_='topic-body__title')
        date_time = document.findAll('a', class_='topic-header__time')
        content = document.findAll('div', class_='topic-body__content')
        article = Article(Utils.wrap('  ' + title[0].text))
        article.datetime = '  ' + date_time[0].text
        article.content = Utils.wrap(Utils.process_links(content[0]).text)
        return (article,)

    def format(self, articles: tuple[Article]) -> str:
        return "\n\n\n".join(map(lambda a: f"{a.datetime}\n{a.title}\n\n{a.content}", articles))


class GoogleSearchExtractor(AbstractExtractor):

    def check(self, url: str, document: Soup):
        return "google.com/search?q=" in url

    def parse(self, document: Soup):
        links = document.select("a:has(h3)", href=True)
        articles = []
        for link in links:
            title = link.find('h3').text
            href = link['href']
            articles.append(Article(Utils.wrap(f"{title} [{href}]")))
        return tuple(articles)

    def format(self, articles: tuple[Article]) -> str:
        return "\n\n\n".join(map(lambda a: f"{a.title}", articles))


class RiaExtractor(AbstractExtractor):

    def check(self, url: str, document: Soup):
        return "https://ria.ru/" in url

    def parse(self, document: Soup):
        title = document.findAll('div', class_='article__title')
        date_time = document.findAll('div', class_='article__info-date')
        content = document.findAll('div', class_='article__body')
        article = Article(Utils.wrap('  ' + title[0].text))
        article.datetime = date_time[0].text
        article.content = Utils.wrap(Utils.process_links(content[0]).text)
        return (article,)

    def format(self, articles: tuple[Article]) -> str:
        return "\n\n\n".join(map(lambda a: f"{a.datetime}\n{a.title}\n\n{a.content}", articles))


class Utils:

    @staticmethod
    def wrap(text):
        return "\n".join(textwrap.wrap(text, 80))

    @staticmethod
    def process_links(element: Tag):
        links = element.select('a', href=True)
        for link in links:
            if link.has_attr('href'):
                href = link['href']
                text = f"{link.text}[{unquote(href)}]" if not href.startswith('#') else link.text
                link.replaceWith(text)
            else:
                link.replaceWith(link.text)
        return element
