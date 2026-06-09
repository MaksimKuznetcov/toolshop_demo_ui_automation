import allure

class CatalogPage:
    def __init__(self, page):
        self.page = page
        
        # Локатор пункта меню Hand Tools из выпадающего списка Categories
        self.categories = page.locator('[data-test="nav-categories"]')
        self.hand_tools = page.locator('[data-test="nav-hand-tools"]')
        
        # Локатор выпадающего списка сортировки
        self.sort_dropbox = page.locator('[data-test="sort"]')
        
        # Локатор чекбокса Hammer
        self.checkbox_hammer = page.get_by_label("Hammer")
        
        # Локатор товара Thor Hammer
        self.product_thor_hammer = page.locator('a[data-test^="product-"]').filter(has_text="Thor Hammer")
        
        # Локатор кнопки Add to cart
        self.add_to_cart_button = page.locator('[data-test="add-to-cart"]')
        
        # Локатор ссылки для перехода в корзину
        self.go_to_cart_link = page.locator('[data-test="nav-cart"]')
        
        # Локатор для проверки наличия товара в корзине
        self.product_title = page.locator('[data-test="product-title"]')
        
    @allure.step("Перейти в категорию Hand Tools из выпадающего списка Categories")
    def go_to_hand_tools(self):
        self.categories.click()
        self.hand_tools.click()    
        
    @allure.step("Сделать сортировку и фильтрацию товара")
    def sort_and_filter(self):
        self.sort_dropbox.select_option(value="price,asc")
        self.checkbox_hammer.check()

    @allure.step("Выбрать товар и перейти на страницу товара")
    def go_to_product(self):
        self.product_thor_hammer.click()
    
    @allure.step("Добавить товар в корзину и сделать переход в корзину")
    def add_to_cart(self):
        self.add_to_cart_button.click()
        self.go_to_cart_link.click()