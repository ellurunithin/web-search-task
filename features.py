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


class Indexer:
    def __init__(self):
        self.index = defaultdict(list)

    def index_page(self, url, text):
        words = re.findall(r'\b\w+\b', text.lower())
        stop_words = {'and', 'the', 'in', 'of', 'a'}  # Example stop words
        words = [word for word in words if word not in stop_words]

        for word in words:
            self.index[word].append(url)

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
