from playwright.sync_api import expect
import pytest
import re
from pages.advanced_search_page import AdvancedSearchPage
from pages.search_results_page import SearchResultsPage
from pages.author_details_page import AuthorDetailsPage

@pytest.mark.ui
@pytest.mark.parametrize(
    "title, author, author_full_name, sort_by, expected_top_rated_work",
    [
        ("Harry Potter", "Rowling", "J. K. Rowling","Rating","Harry Potter and the Half-Blood Prince"),
    ],
)
def test_author_top_rated_book(page, title, author, author_full_name, sort_by, expected_top_rated_work):
    advanced_search_page = AdvancedSearchPage(page)
    search_results_page = SearchResultsPage(page)
    author_details_page = AuthorDetailsPage(page)
    
    # Step 1 — Advanced search
    advanced_search_page.open()
    advanced_search_page.search(title=title, author=author)
    
    expect(page).to_have_url(re.compile(r".*/search\?.*"))

    # Step 2 — Verify results exist for author and click first result then verify author details page
    assert search_results_page.result_count() > 0, f"No results found for title='{title}', author='{author}'"

    first_result_author = search_results_page.get_result_author(0)
    assert author.lower() in first_result_author.lower(), f"Expected author '{author}' in first result, but got '{first_result_author}'"
    
    search_results_page.click_author(0)
    expect(page).to_have_url(re.compile(r"openlibrary\.org/authors"))
    expect(author_details_page.author_name).to_have_text(re.compile(author_full_name))
    
    # Step 3 — On authors page sort works by rating and verify top rated work
    author_details_page.sort_by(sort_by)

    # Step 4 — Validate top-rated work
    top_work = author_details_page.get_top_rated_book_title()
    assert expected_top_rated_work.lower() in top_work.lower(), f"Expected top-rated work '{expected_top_rated_work}', but got '{top_work}'"