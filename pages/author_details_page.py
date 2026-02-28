from pages.base_page import BasePage

class AuthorDetailsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.author_name = page.locator("h1")
        self.sort_dropdown = page.locator("details.sort-dropper summary.tool-button")
        self.book_titles = page.locator("li.searchResultItem.sri--w-main h3.booktitle a.results")
    
    def sort_by(self, option_value: str) -> None:
        sort_option = self.page.locator(f"a[data-ol-link-track='SearchSort|{option_value}']")
        super().sort_by(self.sort_dropdown, sort_option)
         # Wait for results to refresh
        self.book_titles.first.wait_for(state="visible", timeout=15000)

    def get_top_rated_book_title(self) -> str:
        EXCLUDED_KEYWORDS = ["Collection", "Box Set", "Series"]
        self.book_titles.first.wait_for(state="visible")
        count = self.book_titles.count()
        for i in range(count):
            title = self.book_titles.nth(i).inner_text().strip()
            if not any(keyword in title for keyword in EXCLUDED_KEYWORDS):
                return title
        return ""