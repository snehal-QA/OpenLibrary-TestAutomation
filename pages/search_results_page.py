from pages.base_page import BasePage

class SearchResultsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Locators
        self.result_items = page.locator("li.searchResultItem")
        self.sort_dropdown = page.locator("details.sort-dropper summary")

    def result_count(self) -> int:
        return self.result_items.count()
        
    def get_result_author(self, index: int) -> str:
        author_locator= self.result_items.nth(index).locator("a.searchResultAuthor, span.bookauthor a")
        return author_locator.first.inner_text().strip() if author_locator.count() else ""

    def click_author(self, index: int = 0) -> None:
        author_locator = self.result_items.nth(index).locator("a.searchResultAuthor, span.bookauthor a").first
        author_locator.wait_for(state="visible")
        author_locator.click()

    def sort_by(self, option_value: str) -> None:
        self.sort_by_track_value(self.sort_dropdown, option_value, self.result_items)  
        
    def get_result_title(self, index: int = 0) -> str:
        title_locators = self.result_items.locator("a.results")
        return self.get_first_valid_title(title_locators, start=index)
