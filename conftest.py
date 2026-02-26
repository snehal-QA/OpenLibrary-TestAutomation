import pytest
import os

@pytest.fixture(scope="session")
def base_url():
    return "https://openlibrary.org"

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 800},
        "locale": "en-US",
    }

@pytest.fixture(autouse=True)
def trace_each_test(context, browser_name, request):
    os.makedirs("traces", exist_ok=True)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield
    trace_path = f"traces/{browser_name}_{request.node.name}.zip"
    context.tracing.stop(path=trace_path)