from playwright.sync_api import Page, Locator
from pages.base_page import BasePage

class AuthorDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.author_name = page.locator("h1")
        self.sort_dropdown = page.locator("details.sort-dropper summary.tool-button")
        self.works_list = page.locator("ul.list-books")
        self.work_rows = page.locator("li.searchResultItem.sri--w-main")
        self.book_titles = page.locator("li.searchResultItem.sri--w-main h3.booktitle a.results")
    
    def sort_by(self, option_value: str) -> None:
        self.sort_dropdown.wait_for(state="visible")
        self.sort_dropdown.click()
        locator = self.page.locator(f"a[data-ol-link-track='SearchSort|{option_value}']")
        locator.wait_for(state="visible")
        locator.click()

    def get_top_rated_book_title(self) -> str:
        EXCLUDED_KEYWORDS = ["Collection", "Box Set", "Series"]
        self.book_titles.first.wait_for(state="visible")
        count = self.book_titles.count()
        for i in range(count):
            title = self.book_titles.nth(i).inner_text().strip()
            if not any(keyword in title for keyword in EXCLUDED_KEYWORDS):
                return title
        return ""