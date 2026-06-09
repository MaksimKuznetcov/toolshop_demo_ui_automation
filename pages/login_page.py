import allure

class LoginPage:
    def __init__(self, page):
        self.page = page
        
        # Локатор ссылки Sign in
        self.sign_in_link = page.locator('[data-test="nav-sign-in"]')
        
        # Локаторы формы авторизации
        self.email_input = page.locator('[data-test="email"]')
        self.password_input = page.locator('[data-test="password"]')
        self.login_button = page.locator('[data-test="login-submit"]')
        
    @allure.step("Открыть главную страницу сайта")
    def navigate(self):
        self.page.goto('https://practicesoftwaretesting.com')

    @allure.step("Кликнуть по ссылке Sign in")
    def click_sign_in(self):
        self.sign_in_link.click()
    
    @allure.step("Заполнить форму авторизации и выполнить вход")
    def login(self, email, password):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
    