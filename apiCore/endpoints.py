class Endpoints:
    BASE_URL = "https://openlibrary.org"
    SEARCH_BOOKS = f"{BASE_URL}/search.json"
    GET_AUTHOR_DETAILS = f"{BASE_URL}/authors/{{author_key}}.json"