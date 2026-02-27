from pages.advanced_search_page import AdvancedSearchPage
from pages.search_results_page import SearchResultsPage
from pages.author_details_page import AuthorDetailsPage

class PageFactory:

    def __init__(self, page):
        self.page = page
        self.advanced_search_page = AdvancedSearchPage(page)
        self.search_results_page = SearchResultsPage(page)
        self.author_details_page = AuthorDetailsPage(page)