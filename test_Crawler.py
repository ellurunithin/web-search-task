from Crawler import Indexer , Crawler, RankingAlgorithm
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re
import os
import nltk  # Importing nltk for natural language processing
from nltk.corpus import stopwords  # Importing stopwords from NLTK
def main():
    # Get seed URL from user
    seed_url = input("Enter the seed URL: ")

    # Get query from user
    query = input("Enter the query: ")

    # Initialize objects
    crawler = Crawler()
    indexer = Indexer()
    ranking_algorithm = RankingAlgorithm(indexer.index)

    # Crawling and indexing
    links = crawler.crawl(seed_url)
    for link in links:
        if link is not None and link.startswith('http'):
            response = requests.get(link)
            if response.status_code == 200:
                indexer.index_page(link, response.text)

    # Ranking
    page_scores = ranking_algorithm.rank_pages(query)
    print("Ranked Pages:")
    for url, score in page_scores.items():
        print(f"{url}: {score} occurrences of '{query}'")

if __name__ == "__main__":
    main()