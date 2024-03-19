import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re
import os

class Indexer:
    def __init__(self):
        self.index = defaultdict(list)

    def index_page(self, url, text):
        words = re.findall(r'\b\w+\b', text.lower())
        stop_words = {'and', 'the', 'in', 'of', 'a'}  # Example stop words
        words = [word for word in words if word not in stop_words]

        for word in words:
            self.index[word].append(url)