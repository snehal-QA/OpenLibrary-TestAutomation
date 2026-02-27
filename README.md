# OpenLibrary Test Automation Framework

A skeleton test automation framework for validating the [Open Library](https://openlibrary.org) web application at both UI and API levels.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.11+ |
| UI Testing | Playwright (pytest-playwright) |
| API Testing | Requests |
| Test Runner | pytest |
| Reporting | pytest-html |

**Why this stack?** See the [rationale](#rationale) section below.

---

## Project Structure

```
├── apiCore/
│   ├── crudMethods.py        # HTTP client wrapper (requests.Session)
│   └── endpoints.py          # Centralised endpoint constants
├── pages/
│   ├── base_page.py          # Shared page actions (navigate, fill, sort)
│   ├── advanced_search_page.py
│   ├── search_results_page.py
│   ├── author_details_page.py
│   └── page_factory.py       # Single access point for all page objects
├── tests/
│   ├── api/
│   │   └── test_api.py
│   └── ui/
│       └── test_ui.py
├── reports/                  # Auto-generated HTML reports
├── traces/                   # Playwright traces (saved on failure only)
├── conftest.py               # Fixtures and hooks
├── pytest.ini                # pytest configuration
└── requirements.txt
```

---

## Prerequisites

- Python 3.14
- pip

---

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/snehal-QA/OpenLibrary-TestAutomation.git
cd OpenLibrary-TestAutomation

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Playwright browsers
playwright install
```

---

## Running the Tests

```bash
# Run all tests
pytest

# Run only API tests
pytest -m api

# Run only UI tests
pytest -m ui

# Run in headed mode (watch the browser)
pytest -m ui --headed

# Run against a specific browser
pytest -m ui --browser firefox

#Run against all browsers
pytest -m ui --browser chromium --browser firefox --browser webkit
```

After any run, open `reports/report.html` in your browser to view the full HTML report.

If a UI test fails, a Playwright trace file is saved under `traces/`. You can inspect it with:

```bash
playwright show-trace traces/<trace_file>.zip
```
or 
Open https://trace.playwright.dev/ in chrome and drop the trace_zip.file from traces/<trace_file>.zip

---

## Test Coverage

### API Tests
| # | Description |
|---|---|
| 1 | Search for *Harry Potter* by Rowling → validate J.K. Rowling's website URL from author details |
| 2 | Verify `numFound` matches the number of docs returned in search response |
| 3 | Verify search returns zero results for a invalid query |

### UI Tests
| # | Description |
|---|---|
| 1 | Advanced search → click author → sort by rating → validate top-rated book is *Harry Potter and the Half-Blood Prince* |
| 2 | Cross-validate that the top-rated book is consistent between search results page and the author details page |

> All tests are **parametrised**, making it straightforward to extend them for other authors or books.

---

## Rationale

### Why Playwright?
Playwright has become the go-to choice for modern web UI automation. It handles dynamic content and network interception out of the box, has built-in tracing for debugging failures, and offers a reliable auto-wait mechanism that significantly reduces flakiness compared to Selenium. The Python binding pairs naturally with pytest.

### Why Requests for API?
The `requests` library is the standard for HTTP testing in Python — lightweight, readable, and well-understood by any engineer who picks up the project. For this scope it was the right fit; `httpx` would be the next consideration if async support became a requirement.


### Alternatives considered
- **Selenium** — more verbose, requires explicit waits, lacks built‑in tracing and auto‑waiting, which increases flakiness for modern dynamic UIs.
- **JavaScript** — powerful, but adds extra tooling overhead (Node, npm, TS/JS setup). Python provides cleaner readability and faster development for a test‑focused project.
- **Robot Framework** — introduces a DSL layer that adds abstraction and reduces direct control, which is unnecessary for a small, code‑centric assessment.
- **Playwright API** — testing module — tightly coupled to the browser context and not ideal for standalone API testing. Requests is lighter, more explicit, and keeps UI and API layers decoupled.

## What Could Be Improved / Future Work

The framework is intentionally designed to be scalable — the structure, layering, and patterns are all in place. The items below are natural next steps that can be added without reworking anything fundamental.

**Parallel execution**
Plugging in `pytest-xdist` would allow tests to run concurrently across workers, cutting suite execution time significantly as the test count grows. The current fixture design is already compatible with this.

**Richer reporting integrations**
`pytest-html` does the job for a skeleton, but integrating with something like Allure Report would give much more actionable output — step-level breakdowns, trend history across runs, and better attachment handling for traces and screenshots. An Allure report also looks a lot more professional when shared with stakeholders.

**Layered conftest.py structure**
Currently there is a single `conftest.py` at the root. A cleaner approach is one base-level `conftest.py` for shared fixtures (browser config, tracing hooks), a separate one under `tests/ui/` for UI-specific fixtures, and another under `tests/api/` for API-specific ones. This avoids coupling and makes each layer independently maintainable.

**Cross-layer (UI + API) tests**
Some of the most valuable tests combine both layers — for example, using the API to set up or verify state, then validating the result through the UI (or vice versa). A dedicated `tests/integration/` folder with its own `conftest.py` would be the right home for these.

**Broader test coverage**
There is room to go deeper — pagination behaviour, searching by ISBN, author pages with no external website, edge cases with special characters, and verifying that book cover images actually load. Each of these covers a real user journey.

**CI/CD integration**
A GitHub Actions workflow would run the full suite on every push and pull request, with the HTML report and any failure traces published as artefacts automatically.

**Environment configuration**
The base URL and other environment-specific values can be moved into a `.env` file — `python-dotenv` is already in the requirements. This makes switching between local, staging, and production a one-line change with no code edits.
