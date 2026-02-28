import logging
import pytest
from apiCore.endpoints import Endpoints

logger = logging.getLogger(__name__)

@pytest.mark.parametrize(
    "search_params, expected_author_name, expected_website_url",
    [
        ({"title": "Harry Potter", "author": "Rowling"}, "J. K. Rowling", "http://www.jkrowling.com/"),
    ],
)
@pytest.mark.api
def test_author_website_url_is_correct_for_first_book_search(api_client, search_params, expected_author_name, expected_website_url):

    # 1. Search for the book by title and author
    search_book_response = api_client.get_operation(
        Endpoints.SEARCH_BOOKS,
        query_params=search_params
    )
    assert search_book_response.status_code == 200, f"Expected 200 but got {search_book_response.status_code}"
    search_book_data = search_book_response.json()
    assert search_book_data["numFound"] > 0, "No books found"

    # 2. Validate the first result
    first_book = search_book_data["docs"][0]
    assert expected_author_name in first_book["author_name"], (
        f"Expected '{expected_author_name}' but got {first_book['author_name']}"
    )

    # 3. Validate author key exists & extract author key
    assert "author_key" in first_book and first_book["author_key"], "Author key is missing from search result"
    author_key = first_book["author_key"][0]
    logger.info("Extracted author key: %s", author_key)

    # 4. Get author details using author key
    author_details_response = api_client.get_operation(
        Endpoints.GET_AUTHOR_DETAILS.format(author_key=author_key)
    )
    assert author_details_response.status_code == 200, f"Expected 200 but got {author_details_response.status_code}"
    author_details = author_details_response.json()
    logger.debug("Author details response body: %s", author_details)

    # 5. Validate the website URL in author details
    assert author_details.get("links"), "No links found in author details"
    actual_website_url = author_details["links"][0]["url"]
    assert expected_website_url in actual_website_url, (
        f"Expected '{expected_website_url}' but got '{actual_website_url}'"
    )

@pytest.mark.api
@pytest.mark.parametrize(
    "search_params",
    [
        ({"title": "Harry Potter", "author": "Rowling"}),
    ],
)
def test_paginated_docs_count_never_exceeds_total_results_found(api_client, search_params):
    search_book_response = api_client.get_operation(
        Endpoints.SEARCH_BOOKS,
        query_params=search_params
    )

    assert search_book_response.status_code == 200, f"Expected 200 but got {search_book_response.status_code}"
    
    response = search_book_response.json()
    assert response["numFound"] > 0, "No results found"
    assert len(response["docs"]) > 0, "Docs array is empty"
    assert len(response["docs"]) <= response["numFound"], (
        f"Docs returned ({len(response['docs'])}) exceeds numFound ({response['numFound']})"
    )

@pytest.mark.parametrize(
    "search_params",
    [
        ({"title": "xyzabc123456", "author": "xyz123456"}),
    ],
)
@pytest.mark.api
def test_search_returns_no_results_for_invalid_query(api_client, search_params):

    # Step 1 — Search with a invalid query
    search_book_response = api_client.get_operation(
        Endpoints.SEARCH_BOOKS,
        query_params=search_params
    )
    assert search_book_response.status_code == 200, f"Expected 200 but got {search_book_response.status_code}"
    search_book_data = search_book_response.json()

    # Step 2 — Validate no results are returned
    assert search_book_data["numFound"] == 0, (
        f"Expected no results but got {search_book_data['numFound']}"
    )
    assert search_book_data["docs"] == [], "Expected empty docs list but got results"    