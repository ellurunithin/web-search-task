from flask import Flask, request, jsonify
import requests
import nltk
from nltk.corpus import stopwords
from Crawler import Crawler, Indexer, RankingAlgorithm

app = Flask(__name__)

# Download NLTK stop words data
nltk.download('stopwords')

# Define stop words list using NLTK
stop_words = set(stopwords.words('english'))

# Initialize objects
crawler = Crawler()
indexer = Indexer(stop_words)  # Pass stop words list to the Indexer constructor
ranking_algorithm = RankingAlgorithm(indexer.index)
welcome_message = "Welcome to the Crawl and Rank API!"

@app.route('/',methods=['GET'])
def welcome():
    print(welcome_message)  # Print welcome message in the terminal
    return welcome_message

@app.route('/search', methods=['GET','POST'])
def search():
    
    if request.method == 'GET':
        print("Received a request!")  # Print message indicating a request has been received
        # Hardcoded seed_url and query
        seed_url = "https://www.msit.ac.in/"
        query = "murthy"

        # Crawling and indexing
        links = crawler.crawl(seed_url)
        for link in links:
            if link is not None and link.startswith('http'):
                response = requests.get(link)
                if response.status_code == 200:
                    indexer.index_page(link, response.text)
        # Ranking
        page_scores = ranking_algorithm.rank_pages(query)
        for page, score in page_scores.items():
            print(f"{page}")
        return jsonify(page_scores)
    else:
        print("Method not allowed!")  # Print message indicating the method is not allowed
        return jsonify({"error": "Method not allowed"}), 405

if __name__ == '__main__':
    app.run(debug=True)
