from main import WebCrawler
import unittest
from unittest.mock import patch, MagicMock
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse

class WebCrawlerTests(unittest.TestCase):
    @patch('requests.get')
    def test_crawl_success(self, mock_get):
        sample_html = """
        <html><body>
            <h1>Welcome!</h1>
            <a href="/about">About Us</a>
            <a href="https://www.external.com/about">External Link</a> 
            <a href="https://www.external.com">External Link</a>
        </body></html>
        """

        # added an extra line in sample_html
        mock_response = MagicMock()
        mock_response.text = sample_html
        mock_get.return_value = mock_response

        crawler = WebCrawler()
        crawler.crawl("https://www.external.com")

        # Assert that 'about' was added to visited URLs
        self.assertIn("https://www.external.com/about", crawler.visited)

    @patch('requests.get')
    def test_crawl_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Test Error")

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        # Assertions to check if the error was logged (you'll
        # likely need to set up logging capture in your tests)

    # adding an extra method to avoid the error message while crawling.
    @patch('requests.get')
    def test_crawl_external_link(self, mock_get):
        sample_html = """
        <html><body>
            <h1>Welcome!</h1>
            <a href="/about">About Us</a>
            <a href="https://www.external.com">External Link</a>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.text = sample_html
        mock_get.return_value = mock_response

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        # Assert that external links are not added to visited URLs
        self.assertNotIn("https://www.external.com", crawler.visited)
        results = crawler.search("keyword")
        #In this case, it is expected that both "page1" and "page2" are returned in the search results.
        self.assertEqual(results, ["page1","page2"])
    
    def test_search_with_keyword_present(self):
        crawler=WebCrawler()
        crawler.index["page1"]="This page contains the keyword multiple times. keyword keyword"
        crawler.index["page2"]="No keyword here"
        # Search for the keyword and assert the results weather the given keyword is present or not.
        results=crawler.search("keyword")
        self.assertEqual(results,["page1","page2"])
    def test_search_keyword_present_case_insensitive(self):
        crwaler=WebCrawler()
        crwaler.index["page1"]="This page contains the keyword in lowercase"
        crwaler.index["page2"]="No keyword here"
        # Search for the keyword in a case-insensitive manner and assert the results
        results=crwaler.search("KEYWORD")
        self.assertEqual(results,["page1","page2"])
    def test_search_keyword_notpresent(self):
        crawler=WebCrawler()
        crawler.index["page1"]="This page conatians the keyword"
        crawler.index["page2"]="No keyword here"
        # Search for a keyword that is not present and assert an empty result
        results=crawler.search("head")
        self.assertEqual(results,[])
    def test_search_empty_index(self):
        crawler=WebCrawler()
        results=crawler.search("keyword")
        self.assertEqual(results,[])
    def test_search_with_multiple_occurrences(self):
        # Test searching for a keyword with multiple occurrences on the same page
        crawler = WebCrawler()
        crawler.index["page1"] = "This page contains the keyword multiple times. keyword keyword"
        results = crawler.search("keyword")
        self.assertEqual(results, ["page1"])
    def test_search_with_special_characters(self):
        # Test searching for a keyword with special characters
        crawler = WebCrawler()
        crawler.index["page1"] = "This page contains the @special#keyword!"
        results = crawler.search("@special#keyword")
        self.assertEqual(results, ["page1"])
    def test_search_with_empty_keyword(self):
        # Test searching with an empty keyword
        crawler = WebCrawler()
        crawler.index["page1"] = "Thispagecontainssomecontent"
        crawler.index["page2"]=" "
        results = crawler.search(" ")
        self.assertEqual(results, ["page2"])
    def test_search_case_sensitive(self):
        # Test searching for a keyword in a case-sensitive manner
        crawler = WebCrawler()
        crawler.index["page1"] = "This page contains the KeyWord"
        results = crawler.search("keyword")
        self.assertNotEqual(results,[])

    @patch('sys.stdout')
    def test_print_results(self, mock_stdout):
        crawler = WebCrawler()
        crawler.print_results(["https://test.com/result"])

        # Assert that the output was captured correctly by mock_stdout

unittest.main()  # Run unit tests


