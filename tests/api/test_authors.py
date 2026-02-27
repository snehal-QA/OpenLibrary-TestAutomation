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
def test_author_website_url_is_correct_for_book_search(api_client, search_params, expected_author_name, expected_website_url):

    # 1. Search for the book by title and author
    search_book_response = api_client.get_operation(
        Endpoints.SEARCH_BOOKS,
        query_params=search_params
    )
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
    author_details = author_details_response.json()
    logger.debug("Author details response body: %s", author_details)

    # 5. Validate the website URL in author details
    assert author_details.get("links"), "No links found in author details"
    actual_website_url = author_details["links"][0]["url"]
    assert expected_website_url in actual_website_url, (
        f"Expected '{expected_website_url}' but got '{actual_website_url}'"
    )