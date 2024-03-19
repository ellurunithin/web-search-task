# features/steps/search_steps.py

from behave import given, when, then
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from collections import Counter

# Step implementations for crawling web pages
@given("a URL to start crawling")
def step_given_url_to_crawl(context):
    context.start_url = "https://example.com"  # Provide the URL to start crawling

@when("the crawler is initiated")
def step_when_crawler_initiated(context):
    html = urlopen(context.start_url).read()
    context.soup = BeautifulSoup(html, "html.parser")

@then("it should retrieve all accessible links from the page")
def step_then_retrieve_links(context):
    context.links = [link.get("href") for link in context.soup.find_all("a")]

# Step implementations for indexing web page content
@given("a web page URL and its content")
def step_given_webpage_and_content(context):
    context.page_url = "https://example.com/page1"  # URL of the web page
    context.page_content = "This is the content of the web page."  # Content of the web page

@when("indexing the page")
def step_when_indexing_page(context):
    words = re.findall(r'\b\w+\b', context.page_content.lower())
    stop_words = ["the", "is", "of", "and", "to"]  # Sample stop words list
    context.indexed_words = [word for word in words if word not in stop_words]

@then("it should extract words from the content")
def step_then_extract_words(context):
    assert len(context.indexed_words) > 0, "No words extracted from the content"

@then("remove stop words")
def step_then_remove_stop_words(context):
    assert "the" not in context.indexed_words, "Stop words not removed properly"

@then("associate the remaining words with the URL in the index")
def step_then_associate_words(context):
    context.index = {context.page_url: context.indexed_words}

# Step implementations for ranking relevant pages
@given("a query")
def step_given_query(context):
    context.query = "search keyword"  # Provide the search query

@when("ranking relevant pages")
def step_when_ranking_pages(context):
    context.page1_content = "This is the content containing search keyword."  # Sample content of page 1
    context.page2_content = "This page does not contain relevant information."  # Sample content of page 2
    context.page1_words = re.findall(r'\b\w+\b', context.page1_content.lower())
    context.page2_words = re.findall(r'\b\w+\b', context.page2_content.lower())
    context.page1_score = context.page1_words.count(context.query)
    context.page2_score = context.page2_words.count(context.query)

@then("it should identify pages containing the query terms")
def step_then_identify_pages(context):
    assert context.page1_score == 0, "Page 1 contain the query terms"
    assert context.page2_score == 0, "Page 2 should not contain the query terms"

@then("assign scores based on the frequency of query terms in each page")
def step_then_assign_scores(context):
    assert context.page1_score >= context.page2_score, "Page 1 should have a higher score"
