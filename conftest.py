import pytest
import os
from apiCore.crudMethods import CrudMethods
from pages.page_factory import PageFactory

# create required folders for reports and traces before any tests run
def pytest_configure(config):
    os.makedirs("reports", exist_ok=True)
    os.makedirs("traces", exist_ok=True)

# Hook to capture test result- needed to know if test failed
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)    

# Playwright browser customization
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 800},
        "locale": "en-US",
    }

# Trace only UI tests, and save only on failure to save disk space
@pytest.fixture(autouse=True)
def trace_each_test(request):  
    if not request.node.get_closest_marker("ui"):
        yield
        return
    
    context = request.getfixturevalue("context")
    browser_name = request.getfixturevalue("browser_name")

    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield
    
    # save trace only on failure to save disk space
    failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
    if failed:
        trace_path = f"traces/{browser_name}_{request.node.name}.zip"
        context.tracing.stop(path=trace_path)
    else:
        context.tracing.stop()

@pytest.fixture
def web_app(page):
    return PageFactory(page)

# API client fixture
@pytest.fixture
def api_client():
    client = CrudMethods()
    yield client
    client.close()    

def pytest_configure(config):
    if hasattr(config, "_metadata"):
        config._metadata["Project"] = "OpenLibrary Test Automation"
        config._metadata["Base URL"] = "https://openlibrary.org"
        config._metadata["Browser"] = "Chromium"
        config._metadata["Test Types"] = "API, UI"   