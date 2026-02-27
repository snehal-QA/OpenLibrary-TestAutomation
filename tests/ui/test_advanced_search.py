from playwright.sync_api import expect
import pytest
import re
import logging

logger = logging.getLogger(__name__)

@pytest.mark.ui
@pytest.mark.parametrize(
    "title, author, author_full_name, sort_by, expected_top_rated_work",
    [
        ("Harry Potter", "Rowling", "J. K. Rowling","Rating","Harry Potter and the Half-Blood Prince"),
    ],
)
def test_author_top_rated_book(web_app, title, author, author_full_name, sort_by, expected_top_rated_work):
    
    # Step 1 — Advanced search
    web_app.advanced_search_page.open()
    web_app.advanced_search_page.search(title=title, author=author)
    
    # Step 2 — Verify results exist for author and click first result then verify author details page
    assert web_app.search_results_page.result_count() > 0, f"No results found for title='{title}', author='{author}'"

    first_result_author = web_app.search_results_page.get_result_author(0)
    assert author.lower() in first_result_author.lower(), f"Expected author '{author}' in first result, but got '{first_result_author}'"
    
    web_app.search_results_page.click_author(0)
    expect(web_app.page).to_have_url(re.compile(r"openlibrary\.org/authors"))
    expect(web_app.author_details_page.author_name).to_have_text(re.compile(author_full_name))
    
    # Step 3 — On authors page sort works by rating and verify top rated work
    web_app.author_details_page.sort_by(sort_by)

    # Step 4 — Validate top-rated work
    top_work = web_app.author_details_page.get_top_rated_book_title()
    assert expected_top_rated_work.lower() in top_work.lower(), f"Expected top-rated work '{expected_top_rated_work}', but got '{top_work}'"


@pytest.mark.ui
@pytest.mark.parametrize(
    "title, author, author_full_name",
    [
        ("Harry Potter", "Rowling", "J. K. Rowling"),
    ],
)
def test_top_rated_book_is_consistent_across_search_and_author_page(web_app, title, author, author_full_name):

    # Step 1 — Search and sort by rating
    web_app.advanced_search_page.open()
    web_app.advanced_search_page.search(title=title, author=author)
    web_app.search_results_page.sort_by("Rating")
    assert web_app.search_results_page.result_count() > 0, f"No results found for title='{title}'"

    # Step 2 — Grab top result from search
    top_book_from_search = web_app.search_results_page.get_result_title(0)
    logger.info(f"Top rated book from search results: '{top_book_from_search}'")    
    # Step 3 — Navigate to author page
    web_app.search_results_page.click_author(0)
    expect(web_app.page).to_have_url(re.compile(r"openlibrary\.org/authors"))
    expect(web_app.author_details_page.author_name).to_have_text(re.compile(author_full_name))

    # Step 4 — Sort author works by rating
    web_app.author_details_page.sort_by("Rating")

    # Step 5 — Validate top rated book matches across both views
    top_book_from_author_page = web_app.author_details_page.get_top_rated_book_title()
    logger.info(f"Top rated book from author page: '{top_book_from_author_page}'")
    assert top_book_from_search.lower() == top_book_from_author_page.lower(), (
        f"Top rated book mismatch: search shows '{top_book_from_search}' "
        f"but author page shows '{top_book_from_author_page}'"
    )