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


# Макскировка для обхода капчи
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Маскирует браузер под реального пользователя Windows,
    чтобы обойти глухую капчу Cloudflare в GitHub Actions
    """
    return {
        **browser_context_args,
        "viewport": { "width": 1920, "height": 1080 },
        # Подменяем заголовок на стандартный домашний Chrome на Windows 10
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        # Добавляем локаль и языки, чтобы сервер не выдавал пустую EN-локаль дата-центра
        "locale": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        # Говорим хрому игнорировать статус автоматизации
        "ignore_https_errors": True
    }

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """
    Добавляем системные аргументы Chromium, чтобы скрыть 
    автоматическую природу управления браузером от Cloudflare
    """
    return {
        **browser_type_launch_args,
        "args": [
            "--disable-blink-features=AutomationControlled", # Скрывает navigator.webdriver = true
            "--disable-infobars" # Убирает плашку "Браузером управляет автоматизированное ПО"
        ]
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
