from playwright.sync_api import expect
import pytest
import re
from pages.advanced_search_page import AdvancedSearchPage
from pages.search_results_page import SearchResultsPage
from pages.author_details_page import AuthorDetailsPage
from urllib.parse import quote_plus

@pytest.mark.ui
@pytest.mark.parametrize(
    "title, author, authorFullName, sortBy, expected_top_rated_work",
    [
        ("Harry Potter", "Rowling", "J. K. Rowling","Rating","Harry Potter and the Half-Blood Prince"),
    ],
)
def test_author_top_rated_book(page, title, author, authorFullName, sortBy, expected_top_rated_work):
    advanced_search_page = AdvancedSearchPage(page)
    search_results_page = SearchResultsPage(page)
    author_details_page = AuthorDetailsPage(page)
    
    # Step 1 — Advanced search
    advanced_search_page.open()
    advanced_search_page.search(title=title, author=author)
    
    expect(page).to_have_url(re.compile(re.escape(f"/search?title={quote_plus(title)}&author={quote_plus(author)}")))

    # Step 2 — Verify results exist for author and click first result
    assert search_results_page.result_count() > 0

    first_result_author = search_results_page.get_result_author(0)
    assert author.lower() in first_result_author.lower(), f"Expected author '{author}' in first result, but got '{first_result_author}'"
    
    search_results_page.click_author(0)
    # verify we are on the correct author details page
    expect(page).to_have_url(re.compile(r"openlibrary\.org/authors"))
    expect(author_details_page.author_name).to_have_text(re.compile(authorFullName))
    
    # Step 3 — On authors page sort works by rating and verify top rated work
    author_details_page.sort_by(sortBy)

    # Step 4 — Validate top-rated work
    topWork = author_details_page.get_top_rated_book_title()
    assert expected_top_rated_work.lower() in topWork.lower(), f"Expected top-rated work '{expected_top_rated_work}', but got '{topWork}'"