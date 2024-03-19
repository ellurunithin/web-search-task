import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re
import os

class RankingAlgorithm:
    def __init__(self, index):
        self.index = index

    def rank_pages(self, query):
        query_words = query.lower().split()
        relevant_pages = set()
        for query_word in query_words:
            relevant_pages.update(self.index.get(query_word, []))
        scores = {page: sum(page.count(word) for word in query_words) for page in relevant_pages}
        return scores