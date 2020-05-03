import re
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List

@dataclass
class ArticleListing():

    def list_articles(self, page: BeautifulSoup) -> List[str]:
        try:
            soup: BeautifulSoup = self.__create__soup(page)
            links_from_archive: List[str] = self.__get_list_of_articles(soup)
            links_from_archive = self.__remove_unnecessary_links(links_from_archive)
        except Exception as list_generation_error:
            print(f'List generation failed: {list_generation_error}')
        
        return links_from_archive

    def __create__soup(self, page: BeautifulSoup) -> BeautifulSoup:
        soup: BeautifulSoup = BeautifulSoup(page, 'html.parser')
   
        if len(soup) == 0:
            raise Exception('Empty soup!')
        
        return soup
    
    def __get_list_of_articles(self, soup: BeautifulSoup) -> List[str]:
        articles: List[str] = []
        
        links: BeautifulSoup = soup.find_all('figure', class_='post-image-thumbnail')

        for link in links:
            for element in link.find_all('a'):
                articles.append(element.get('href'))

        if len(articles) == 0:
            raise Exception('No articles!')

        return articles
    
    def __remove_unnecessary_links(self, links_from_archive: List[str]) -> List[str]:
        for archive_link in links_from_archive:
            match = re.match(r'https:\/\/dailyweb.pl/category/', archive_link)
            if match != None:
                links_from_archive.remove(archive_link)
        
        if len(links_from_archive) == 0:
            raise Exception('Links archive is empty!')

        return links_from_archive

