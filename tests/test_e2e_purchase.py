import allure
import re
from playwright.sync_api import Page, expect


@allure.feature("Оформление заказа")
@allure.story("Сквозной E2E: Покупка инструментов")
def test_e2e_purchase(page: Page, user_data, login_page, catalog_page, checkout_page):
    
    # Заходим на главную страницу сайта TOOLSHOP DEMO и кликаем Sign in
    login_page.navigate()
    login_page.click_sign_in()

    with allure.step("Проверить успешный переход на этап авторизации"):
        expect(page).to_have_url(re.compile(r".*/auth/login"), timeout=5000)

    # Заполняем форму авторизации и выполняем вход
    login_page.login("customer@practicesoftwaretesting.com", "welcome01")

    with allure.step("Проверить успешный переход на страницу управления аккаунтом"):
        expect(page).to_have_url(re.compile(r".*/account"), timeout=5000)

    # В меню в выпадающем списке Categories кликаем на Hand Tools
    catalog_page.go_to_hand_tools()

    with allure.step("Проверить успешный переход на страницу выбора товара"):
        expect(page).to_have_url(re.compile(r".*/category/hand-tools"), timeout=5000)

    # Делаем сортирвку и фильтрацию
    catalog_page.sort_and_filter()

    with allure.step("Проверть что чекбокс действительно отмечен"):
        expect(catalog_page.checkbox_hammer).to_be_checked()

    # Выбираем товар и переходим на страницу товара
    catalog_page.go_to_product()

    with allure.step("Проверить успешный переход на страницу товара"):
        expect(page).to_have_url(re.compile(r".*/product*"), timeout=5000)

    # Добавляем товар в корзину и делаем переход в корзину
    catalog_page.add_to_cart()
    
    with allure.step("Проверить что товар действительно добавлен в корзину"):
        expect(catalog_page.product_title).to_have_text("Thor Hammer")
    
    # Переходим к оформлению заказа
    checkout_page.proceed_to_checkout()

    with allure.step("Проверить появление формы заполнения данных для доставки"):
        expect(checkout_page.billing_heading).to_be_visible(timeout=5000)
    
    # Заполняем данные для доставки и переходим к оплате
    checkout_page.fill_shipping_details(user_data)

    with allure.step("Проверить появление формы оплаты"):
        expect(checkout_page.payment_heading).to_be_visible(timeout=5000)
    
    # Выбираем способ оплаты и нашимаем кнопку подтверждения
    checkout_page.payment_choice()

    with allure.step("Проверить успешность выполнение заказа"):
        expect(checkout_page.payment_success).to_be_visible(timeout=5000)

