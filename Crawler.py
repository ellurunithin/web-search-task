import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re
import os

class Crawler:
    def __init__(self):
        self.visited_urls = set()

    def crawl(self, url):
        if url in self.visited_urls:
            return []

        self.visited_urls.add(url)
        try:
            if url.startswith('http') or url.startswith('https'):
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    links = [link.get('href') for link in soup.find_all('a')]
                    return links
            elif url.startswith('file://'):
                file_path = url[len('file://'):]
                if os.path.exists(file_path):
                    with open(file_path, 'r') as file:
                        soup = BeautifulSoup(file.read(), 'html.parser')
                        links = [link.get('href') for link in soup.find_all('a')]
                        return links
                else:
                    print(f"File {file_path} does not exist.")
            else:
                print(f"Unsupported URL format: {url}")
        except Exception as e:
            print(f"Failed to crawl {url}: {e}")
        return []
