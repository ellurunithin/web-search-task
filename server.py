from flask import Flask, request, jsonify
from Crawler import Crawler, Indexer, RankingAlgorithm

app = Flask(__name__)

# Initialize objects
crawler = Crawler()
indexer = Indexer(stop_words=[])  # Add your stop words here
ranking_algorithm = RankingAlgorithm(indexer.index)

@app.route('/')
def index():
    return 'Welcome to the Web Search API!'

@app.route('/search', methods=['GET'])
def search():
    url = request.args.get('url')
    keyword = request.args.get('keyword')

    # Perform crawling on the specified URL
    results = crawler.crawl(url)

    # Search for the keyword in the crawled content

    return jsonify({"results": results})

@app.route('/crawl', methods=['POST'])
def crawl():
    data = request.json
    start_url = data.get('start_url')
    if not start_url:
        return jsonify({"error": "Start URL is required"}), 400
    links = crawler.crawl(start_url)
    return jsonify({"links": links})

@app.route('/index', methods=['POST'])
def index_page():
    data = request.json
    url = data.get('url')
    text = data.get('text')
    if not url or not text:
        return jsonify({'error': 'URL and text are required'}), 400
    indexer.index_page(url, text)
    return jsonify({'message': 'Page indexed successfully'})

@app.route('/rank', methods=['POST'])
def rank_pages():
    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    scores = ranking_algorithm.rank_pages(query)
    sorted_scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
    return jsonify({'scores': sorted_scores})

if __name__ == '__main__':
    app.run(debug=True)
