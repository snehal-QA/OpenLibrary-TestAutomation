from playwright.sync_api import Page, Locator


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # Navigation
    def navigate(self, url: str):
        self.page.goto(url, wait_until="load",timeout=30000)

    # Common Actions
    def fill(self, loc: Locator, text: str):
        loc.fill(text)

    # Waits
    def wait_for_element_to_be_visible(self, loc: Locator, timeout: int = 7000):
        loc.wait_for(state="visible", timeout=timeout)

    # Sorting
    def sort_by(self, sort_dropdown: Locator, sort_option: Locator) -> None:
        sort_dropdown.wait_for(state="visible")
        sort_dropdown.click()
        sort_option.wait_for(state="visible")
        sort_option.click()
        # Wait for navigation or DOM update after sort
        self.page.wait_for_load_state("domcontentloaded")