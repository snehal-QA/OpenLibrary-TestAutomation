from pages.base_page import BasePage

advanced_search_url = "https://openlibrary.org/advancedsearch"

class AdvancedSearchPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = advanced_search_url
        # Locators
        self.title_input = page.locator("input[name='title']")
        self.author_input = page.locator("input[name='author']")
        self.search_button = page.locator("button[type='submit']")

    def open(self):
        self.navigate(self.url)
        self.wait_for_element_to_be_visible(self.title_input)
        return self

    def search(self, title: str = "", author: str = ""):
        if title:
            self.fill(self.title_input, title)
        if author:
            self.fill(self.author_input, author)
        self.search_button.click()
        # Wait for search results to load
        self.page.wait_for_load_state("domcontentloaded")
        self.page.locator("li.searchResultItem").first.wait_for(state="visible", timeout=15000)
        return self