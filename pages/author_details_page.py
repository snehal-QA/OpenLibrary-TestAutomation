from pages.base_page import BasePage

class AuthorDetailsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.author_name = page.locator("h1")
        self.sort_dropdown = page.locator("details.sort-dropper summary.tool-button")
        self.book_titles = page.locator("li.searchResultItem.sri--w-main h3.booktitle a.results")
    
    def sort_by(self, option_value: str) -> None:
        self.sort_by_track_value(self.sort_dropdown, option_value, self.book_titles)  
        
    def get_top_rated_book_title(self) -> str:
        return self.get_first_valid_title(self.book_titles)