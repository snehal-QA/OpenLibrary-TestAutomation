from playwright.sync_api import Page, Locator


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # Navigation
    def navigate(self, url: str):
        self.page.goto(url, wait_until="domcontentloaded")

    # Common Actions
    def fill(self, loc: Locator, text: str):
        loc.fill(text)

    # Waits
    def wait_for_element_to_be_visible(self, loc: Locator, timeout: int = 5000):
        loc.wait_for(state="visible", timeout=timeout)