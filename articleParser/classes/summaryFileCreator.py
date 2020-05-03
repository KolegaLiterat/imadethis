import re
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List

@dataclass
class SummaryFileCreator():

    def create_summary_file(self, article_data: List[str]) -> bool:
        is_summary_file_created: bool = False
        
        if self.__save_parsed_article_to_file(article_data[1]):
            self.__remove_unnecessary_text(article_data[0])
            is_summary_file_created = True

        return is_summary_file_created
    
    def __save_parsed_article_to_file(self, article_content: List[str]):
        is_file_with_parsed_article_created: bool = False

        with open('parsed_article.txt', 'w+', encoding='UTF-8') as parsed_article:
            for element in article_content:
                parsed_article.write(element.text)
            is_file_with_parsed_article_created = True
        
        parsed_article.close()

        return is_file_with_parsed_article_created
    
    def __remove_unnecessary_text(self, title: str):
        with open('parsed_article.txt', 'r', encoding='UTF-8') as parsed_article:
            article_content = parsed_article.readlines()

            with open('summary_file.txt', 'a+', encoding='UTF-8') as summary_file:
                summary_file.write(title)
                summary_file.write('\n')
                
                for paragrah in article_content:
                    match = re.match('Powinieneś zobaczyć:', paragrah)

                    if match != None:
                        break
                    else:
                        summary_file.write(paragrah)

            summary_file.close()
        parsed_article.close()


