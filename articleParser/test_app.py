#unit test lib!
import pytest

from classes.pageParser import PageParser
from classes.articleListing import ArticleListing
from classes.articleTextParser import ArticleTextParser
from classes.summaryFileCreator import SummaryFileCreator

test_page = PageParser('https://dailyweb.pl/author/adrian-jaworek/')
test_article = PageParser(
    'https://dailyweb.pl/jak-koronawirus-wplynal-na-branze-gamedev/')
test_listing = ArticleListing()
test_article_parsing = ArticleTextParser()
test_summary_file = SummaryFileCreator()

def test_respone_code():
    assert test_page.get_page_data().status_code == 200

def test_links_list():
    assert len(test_listing.list_articles(test_page.get_page_data().content)) != 0

def test_article_parser():
    assert len(test_article_parsing.get_article_text(test_article.get_page_data().content)) != 0

def test_summary_file_creator():
    test_content = test_article_parsing.get_article_text(test_article.get_page_data().content)

    assert test_summary_file.create_summary_file(test_content) == True