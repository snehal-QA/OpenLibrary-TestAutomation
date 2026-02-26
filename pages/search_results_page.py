from playwright.sync_api import Locator, expect
from pages.base_page import BasePage
from pages.author_details_page import AuthorDetailsPage

class SearchResultsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Locators
        self.result_items = page.locator("li.searchResultItem")
        self.first_result = self.result_items.first

    def result_count(self) -> int:
        return self.result_items.count()
        
    def get_result_author(self, index: int) -> str:
        author_locator= self.result_items.nth(index).locator("a.searchResultAuthor, span.bookauthor a")
        return author_locator.first.inner_text().strip() if author_locator.count() else ""

    def click_author(self, index: int = 0) -> None:
        author_locator = self.result_items.nth(index).locator("a.searchResultAuthor, span.bookauthor a").first
        author_locator.wait_for(state="visible")
        author_locator.click()