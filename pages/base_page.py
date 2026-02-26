from playwright.sync_api import Page, Locator


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # Navigation
    def navigate(self, url: str):
        self.page.goto(url, wait_until="domcontentloaded")

    # Common Actions
    def click(self, loc: Locator):
        loc.click()

    def fill(self, loc: Locator, text: str):
        loc.fill(text)

    def text(self, loc: Locator) -> str:
        return loc.inner_text()

    def is_visible(self, loc: Locator) -> bool:
        return loc.is_visible()

    def select_by_value(self, loc: Locator, value: str):
        loc.select_option(value)

    # Waits
    def wait_for_element_to_be_visible(self, loc: Locator, timeout: int = 5000):
        loc.wait_for(state="visible", timeout=timeout)

    def wait_hidden(self, loc: Locator, timeout: int = 5000):
        loc.wait_for(state="hidden", timeout=timeout)

    def wait_dom_loaded(self):
        self.page.wait_for_load_state("domcontentloaded")