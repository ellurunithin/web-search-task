import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re
import os


class RankingAlgorithm:
    def __init__(self, index, stop_words):
        self.index = index
        self.stop_words = stop_words


    def rank_pages(self, query):
        # Remove stopwords from the query
        query_words = [word for word in query.lower().split() if word not in self.stop_words]
        
        relevant_pages = set()
        for query_word in query_words:
            relevant_pages.update(self.index.get(query_word, []))
        
        scores = {page: sum(page.lower().count(word) for word in query_words) for page in relevant_pages}
        return scores

class Indexer:
    def __init__(self):
        self.index = defaultdict(list)  # Creating a defaultdict to store index data

    def index_page(self, url, text):
        words = re.findall(r'\b\w+\b', text.lower())  # Extracting words from text using regex
        words = [word for word in words if word not in self.stop_words]  # Removing stopwords

        for word in words:  # Looping through each word
            self.index[word].append(url)  # Adding URL to the index dictionary under corresponding word

class Crawler:
    def __init__(self):
        # Initialize a set to store visited URLs to avoid revisiting them
        self.visited_urls = set()

    def crawl(self, url):
        # Check if the URL has been visited before, if yes, return an empty list
        if url in self.visited_urls:
            return []

        # Add the URL to the set of visited URLs
        self.visited_urls.add(url)
        try:
            # If the URL starts with 'http' or 'https', it's a web URL
            if url.startswith('http') or url.startswith('https'):
                # Send a GET request to the URL
                response = requests.get(url)
                # Check if the response status code is 200 (OK)
                if response.status_code == 200:
                    # Parse the HTML content of the response
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Extract all links from the HTML using BeautifulSoup
                    links = [link.get('href') for link in soup.find_all('a')]
                    # Return the list of links found on the page
                    return links
            # If the URL starts with 'file://', it's a local file path
            elif url.startswith('file://'):
                # Extract the file path from the URL
                file_path = url[len('file://'):]
                # Check if the file exists
                if os.path.exists(file_path):
                    # Read the content of the file
                    with open(file_path, 'r') as file:
                        # Parse the HTML content of the file
                        soup = BeautifulSoup(file.read(), 'html.parser')
                        # Extract all links from the HTML using BeautifulSoup
                        links = [link.get('href') for link in soup.find_all('a')]
                        # Return the list of links found in the file
                        return links
                else:
                    # Print a message if the file does not exist
                    print(f"File {file_path} does not exist.")
            else:
                # Print a message for unsupported URL formats
                print(f"Unsupported URL format: {url}")
        except Exception as e:
            # Print an error message if crawling fails
            print(f"Failed to crawl {url}: {e}")
        # Return an empty list if crawling fails or if the URL format is unsupported
        return []


