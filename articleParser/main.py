from classes.pageParser import PageParser
from classes.articleListing import ArticleListing
from classes.articleTextParser import ArticleTextParser
from classes.summaryFileCreator import SummaryFileCreator
import re

def main():
    articles_links = ArticleListing()
    article = ArticleTextParser()
    txt_file = SummaryFileCreator()

    page = PageParser('https://dailyweb.pl/author/adrian-jaworek/')

    data_from_page = page.get_page_data()
    
    if data_from_page != None:
        links_archive = articles_links.list_articles(data_from_page.content)
    else:
        print('Data from page is empty!')
    
    if len(links_archive) != 0:
        for link in links_archive:
            article_page = PageParser(link)
            data_from_article = article_page.get_page_data()
            content_for_summary = article.get_article_text(data_from_article.content)
            txt_file.create_summary_file(content_for_summary)
    else:
        print('Article links list is empty!')

if __name__ == "__main__":
    main()
