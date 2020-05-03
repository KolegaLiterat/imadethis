import re
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List

@dataclass
class ArticleTextParser():
    
    month_in_number: str = '04'

    def get_article_text(self, page: BeautifulSoup):
        article_data: List[str] = []
        
        try:
            soup: BeautifulSoup = self.__create_soup(page)
            
            date: str = self.__get_article_published_date(soup)
            is_needed_for_summary: bool = self.__check_is_article_published_in_specific_month(date)

            if is_needed_for_summary:
                article_title: str = self.__get_title_of_article(soup)
                article_data.append(article_title)

                article_content: BeautifulSoup = self.__get_article_content(soup)
                article_data.append(article_content)

        except Exception as article_error:
            print(f'Error in parsing articile: {article_error}')
        
        return article_data

    def __create_soup(self, page: BeautifulSoup):
        soup: BeautifulSoup = BeautifulSoup(page, 'html.parser')

        if len(soup) == 0:
            raise Exception('Empty soup! Check link!')
            
        return soup
    
    def __get_article_published_date(self, soup: BeautifulSoup):
        date: BeautifulSoup = soup.find_all('span', class_='published updated')

        if len(date) == 0:
            raise Exception('Missing date string')

        return date[0].text

    def __check_is_article_published_in_specific_month(self, date_from_page):
        is_article_published_in_specific_month: bool = True
        
        pattern = r'Opublikowano\s\d+\.(?P<month>\d+)\.\d+'

        match = re.match(pattern, date_from_page)

        if match.group('month') == self.month_in_number: 
            is_article_published_in_specific_month = True

        return is_article_published_in_specific_month
    
    def __get_title_of_article(self, soup: BeautifulSoup):
        title: BeautifulSoup = soup.find_all('h1', class_='title entry-title')

        if len(title) == 0:
            raise Exception('Missing title string!')

        return title[0].text
    
    def __get_article_content(self, soup: BeautifulSoup):
        content: BeautifulSoup = soup.find_all('div', class_='content bass')

        if len(content) == 0:
            raise Exception('Missing article content!')

        return content
