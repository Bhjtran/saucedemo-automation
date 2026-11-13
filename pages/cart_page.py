from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name, [data-test='inventory-item-name']")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "#checkout, [data-test='checkout']")
    CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, "#continue-shopping, [data-test='continue-shopping']")
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, "#first-name, [data-test='firstName']")

    def get_product_names(self):
        return [element.text.strip() for element in self.find_all(self.ITEM_NAMES)]

    def remove_product(self, product_slug):
        remove_locator = (By.CSS_SELECTOR, f"#remove-{product_slug}, [data-test='remove-{product_slug}']")
        before = len(self.get_product_names())
        self.click(remove_locator)
        # Chờ số sản phẩm giảm thay vì chỉ chờ nút biến mất.
        self.wait.until(lambda _driver: len(self.get_product_names()) < before)

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        self.find_visible(self.FIRST_NAME_INPUT)

    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BUTTON)
