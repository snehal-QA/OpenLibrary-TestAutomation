from playwright.sync_api import Page, Locator


class BasePage:
    EXCLUDED_KEYWORDS = ["Collection", "Box Set", "Boxset", "Series"]
    _SORT_TRACK_PREFIX = "SearchSort"

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
    def click_sort_option(self, sort_dropdown: Locator, sort_option: Locator) -> None:
        sort_dropdown.wait_for(state="visible")
        sort_dropdown.click()
        sort_option.wait_for(state="visible")
        sort_option.click()
        # Wait for navigation or DOM update after sort
        self.page.wait_for_load_state("domcontentloaded")

    def sort_by_track_value(self, dropdown: Locator, option_value: str, wait_locator: Locator) -> None:
        sort_option = self.page.locator(
            f"a[data-ol-link-track='{self._SORT_TRACK_PREFIX}|{option_value}']"
        )
        self.click_sort_option(dropdown, sort_option)
        wait_locator.first.wait_for(state="visible", timeout=15000)    

    def get_first_valid_title(self, title_locators, start: int = 0) -> str:
        title_locators.nth(start).wait_for(state="visible")
        for i in range(start, title_locators.count()):
            title = title_locators.nth(i).inner_text().strip()
            if not any(kw in title for kw in self.EXCLUDED_KEYWORDS):
                return title
        return ""    