Feature: Specific website search
    As a user, I want to search a specific website so that I can find relevent informstion quickly
    Scenario 1: Crawling Web Pages
        Given a URL to start crawling
        When the crawler is initiated
        Then it should retrieve all accessible links from the page

    Scenario 2: Indexing Web Page Content
        Given a web page URL and its content
        When indexing the page
        Then it should extract words from the content
        And remove stop words
        And associate the remaining words with the URL in the index

    Scenario 3: Ranking Relevant Pages
        Given a query
        When ranking relevant pages
        Then it should identify pages containing the query terms
        And assign scores based on the frequency of query terms in each page