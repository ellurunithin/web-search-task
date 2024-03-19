import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re
import os


class Indexer:
    def __init__(self):
        self.index = defaultdict(list)  # Creating a defaultdict to store index data

    def index_page(self, url, text):
        words = re.findall(r'\b\w+\b', text.lower())  # Extracting words from text using regex
        stop_words = {'and', 'the', 'in', 'of', 'a'}  # Example stop words
        words = [word for word in words if word not in stop_words]  # Removing stop words

        for word in words:  # Looping through each word
            self.index[word].append(url)  # Adding URL to the index dictionary under corresponding word
