class Endpoints:
    BASE_URL = "https://openlibrary.org"
    SEARCH_BOOKS = f"{BASE_URL}/search.json"
    SEARCH_AUTHORS = f"{BASE_URL}/search/authors.json"
    GET_AUTHOR_DETAILS = f"{BASE_URL}/authors/{{author_key}}.json"