import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

def test_homepage_title(page):
    page.goto("https://engeto.cz")
    assert page.title() == "Engeto - Vzdělávání v IT", "Titulní stránka má špatný titul."

def test_presence_of_main_heading(page):
    page.goto("https://engeto.cz")
    main_heading = page.query_selector("h1")
    assert main_heading is not None, "Hlavní nadpis nebyl nalezen."
    assert main_heading.inner_text() == "Engeto - Vzdělávání v IT", "Hlavní nadpis má špatný text."

def test_search_functionality(page):
    page.goto("https://engeto.cz")
    search_input = page.query_selector("input[name='search']")
    assert search_input is not None, "Vyhledávací pole nebylo nalezeno."
    search_input.fill("Python")
    search_input.press("Enter")
    page.wait_for_timeout(2000)  # Počkejte na načtení výsledků
    results = page.query_selector_all(".search-result")
    assert len(results) > 0, "Žádné výsledky vyhledávání nebyly nalezeny."
