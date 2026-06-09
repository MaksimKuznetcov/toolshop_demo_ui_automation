import pytest
import allure
from faker import Faker


from pages.login_page import LoginPage
from pages.catalog_page import CatalogPage
from pages.checkout_page import CheckoutPage


fake = Faker('en_US')  # Toolshop англоязычный, генерируем US-данные

@pytest.fixture()
def user_data():
    return {
        'postal_code': fake.postcode(),
        'house_number': fake.building_number(),
        'street': fake.street_name(),
        'city': fake.city(),
        'state': fake.state()
    }


# Фикстуры для автоматической инициализации Page Objects
@pytest.fixture()
def login_page(page): return LoginPage(page)

@pytest.fixture()
def catalog_page(page): return CatalogPage(page)

@pytest.fixture()
def checkout_page(page): return CheckoutPage(page)


# Настройка полного экрана
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "no_viewport": True  # Сообщает Playwright, что не нужно принудительно обрезать рамки, позволяя браузеру растянуться на весь физический экран.
    }

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Передает Chromium команду 'запуститься развернутым'"""
    return {
        **browser_type_launch_args,
        "args": ["--start-maximized"]
    }


# Хук для отслеживания упавших тестов и снятия скриншотов
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture(autouse=True)
def attach_screenshot_on_failure(request, page):
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        allure.attach(page.screenshot(full_page=True), name="Failure Screen", attachment_type=allure.attachment_type.PNG)
