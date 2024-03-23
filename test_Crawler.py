import requests
import nltk
from nltk.corpus import stopwords
from Crawler import Crawler, Indexer, RankingAlgorithm

def main():
    # Get seed URL from user
    seed_url = "https://www.msit.ac.in"

    # Get query from user
    query = "murthy"

    # Download NLTK stop words data
    nltk.download('stopwords')

    # Define stop words list using NLTK
    stop_words = set(stopwords.words('english'))

    # Initialize objects
    crawler = Crawler()
    indexer = Indexer(stop_words)  # Pass stop words list to the Indexer constructor
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
        print(f"{url}")

if __name__ == "__main__":
    main()
