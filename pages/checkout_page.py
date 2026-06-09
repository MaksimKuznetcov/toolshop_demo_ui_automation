import allure

class CheckoutPage:
    def __init__(self, page):
        self.page = page
        
        # Локаторы для перехода по процессу оформления заказа
        self.proceed_to_checkout_button = page.locator('[data-test="proceed-1"]')
        self.proceed_to_checkout_button_2 = page.locator('[data-test="proceed-2"]')
        self.proceed_to_checkout_button_3 = page.locator('[data-test="proceed-3"]')

        # Локаторы для подтверждения перехода к следующему этапу оформления заказа
        self.billing_heading = page.locator('h3').filter(has_text="Billing Address")
        self.payment_heading = page.locator('h3').filter(has_text="Payment")

        # Локаторы полей заполнения данных для доставки
        self.country_select = page.locator('[data-test="country"]')
        self.postal_cod_input = page.locator('[data-test="postal_code"]')
        self.house_number_input = page.locator('[data-test="house_number"]')
        self.street_input = page.locator('[data-test="street"]')
        self.city_input = page.locator('[data-test="city"]')
        self.state_input = page.locator('[data-test="state"]')

        # Локатор для выбора оплаты и кнопка подтверждения
        self.payment_select = page.locator('[data-test="payment-method"]')
        self.confirm_button = page.locator('[data-test="finish"]')

        # Локатор для проверки завершения оформления заказа
        self.payment_success = page.locator('[data-test="payment-success-message"]')
    
    @allure.step("Перейти к оформлению заказа")
    def proceed_to_checkout(self):
        self.proceed_to_checkout_button.click()
        self.proceed_to_checkout_button_2.click()
    
    @allure.step("Заполнить форму данными для достаки и переходим к оплате")
    def fill_shipping_details(self, details: dict):
        self.country_select.select_option(value="RU")
        self.postal_cod_input.fill(details['postal_code'])
        self.house_number_input.fill(details['house_number'])
        self.street_input.fill(details['street'])
        self.city_input.fill(details['city'])
        self.state_input.fill(details['state'])
        self.proceed_to_checkout_button_3.click()
    
    @allure.step("Выбрать оплату и подтвердить заказ")
    def payment_choice(self):
        self.payment_select.select_option(value="cash-on-delivery")
        self.confirm_button.click()