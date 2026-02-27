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
        sort_option = self.page.locator(f"a[data-ol-link-track='SearchSort|{option_value}']")
        super().sort_by(self.sort_dropdown, sort_option)    

    def get_result_title(self, index: int) -> str:
        EXCLUDED_KEYWORDS = ["Collection", "Box Set", "Boxset", "Series"]
        count = self.result_items.count()
        for i in range(index, count):
            title_locator = self.result_items.nth(i).locator("a.results")
            if title_locator.count():
                title = title_locator.first.inner_text().strip()
                if not any(keyword in title for keyword in EXCLUDED_KEYWORDS):
                    return title
        return ""