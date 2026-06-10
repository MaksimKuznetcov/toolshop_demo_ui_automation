import pytest
import allure
from playwright_stealth import stealth_sync
from faker import Faker


from pages.login_page import LoginPage
from pages.catalog_page import CatalogPage
from pages.checkout_page import CheckoutPage


fake = Faker('en_US')  # Toolshop англоязычный, генерируем US-данные

@pytest.fixture()
def user_data():
    """Фикстура для генерации динамических валидных данных покупателя."""
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


# НАСТРОЙКИ ОКРУЖЕНИЯ БРАУЗЕРА И МАСКИРОВКИ (STEALTH & ANTI-BOT)
@pytest.fixture(autouse=True)
def apply_stealth(page):
    """
    Автоматическая фикстура (autouse=True), которая выполняется перед каждым тестом.
    Инжектирует маскировочные скрипты в JavaScript-движок каждой новой страницы,
    скрывая автоматическую природу Playwright (удаляет navigator.webdriver и т.д.).
    Необходима для стабильного прохождения защитных фильтров Cloudflare WAF в CI/CD.
    """
    stealth_sync(page)
    yield


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Глобальная сессионная фикстура для конфигурации контекста браузера.
    1. Устанавливает фиксированное Full HD разрешение, предотвращая переход сайта 
       в мобильную верстку (адаптивный дизайн со свернутыми бургер-меню).
    2. Подменяет User-Agent и локаль под реальный десктопный компьютер на Windows 10,
       чтобы избежать блокировок от Cloudflare Turnstile в облачной среде GitHub Actions.
    """
    return {
        **browser_context_args,
        "viewport": { "width": 1920, "height": 1080 },
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "locale": "en-US,en;q=0.9"
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
