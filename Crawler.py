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
