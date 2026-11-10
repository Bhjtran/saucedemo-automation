from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    CART_LINK = (By.CSS_SELECTOR, "a.shopping_cart_link, [data-test='shopping-cart-link']")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge, [data-test='shopping-cart-badge']")
    MENU_BUTTON = (By.CSS_SELECTOR, "#react-burger-menu-btn, [data-test='open-menu']")
    LOGOUT_LINK = (By.CSS_SELECTOR, "#logout_sidebar_link, [data-test='logout-sidebar-link']")
    USERNAME_INPUT = (By.CSS_SELECTOR, "#user-name, [data-test='username']")
    SORT_SELECT = (By.CSS_SELECTOR, "select.product_sort_container, [data-test='product-sort-container']")
    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name, [data-test='inventory-item-name']")
    ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price, [data-test='inventory-item-price']")

    def _product_button(self, action, product_slug):
        return (By.CSS_SELECTOR, f"#{action}-{product_slug}, [data-test='{action}-{product_slug}']")

    def get_cart_count(self):
        badges = self.driver.find_elements(*self.CART_BADGE)
        if not badges:
            return 0
        text = badges[0].text.strip()
        return int(text) if text.isdigit() else 0

    def add_product(self, product_slug):
        add_locator = self._product_button("add-to-cart", product_slug)
        remove_locator = self._product_button("remove", product_slug)
        before = self.get_cart_count()
        button = self.wait.until(EC.presence_of_element_located(add_locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        self.driver.execute_script("arguments[0].click();", button)
        self.wait.until(EC.presence_of_element_located(remove_locator))
        self.wait.until(lambda _driver: self.get_cart_count() >= before + 1)

    def add_backpack(self):
        self.add_product("sauce-labs-backpack")

    def remove_product(self, product_slug):
        remove_locator = self._product_button("remove", product_slug)
        add_locator = self._product_button("add-to-cart", product_slug)
        before = self.get_cart_count()
        button = self.wait.until(EC.presence_of_element_located(remove_locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        self.driver.execute_script("arguments[0].click();", button)
        self.wait.until(EC.presence_of_element_located(add_locator))
        expected = max(0, before - 1)
        self.wait.until(lambda _driver: self.get_cart_count() == expected)

    def open_cart(self):
        link = self.wait.until(EC.presence_of_element_located(self.CART_LINK))
        href = link.get_attribute("href")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
        self.driver.execute_script("arguments[0].click();", link)
        try:
            self.wait.until(EC.any_of(
                EC.visibility_of_element_located((By.XPATH, "//*[normalize-space()='Your Cart']")),
                EC.presence_of_element_located((By.CSS_SELECTOR, "#checkout, [data-test='checkout']")),
            ))
        except Exception:
            if href:
                self.driver.get(href)
                self.wait.until(EC.any_of(
                    EC.visibility_of_element_located((By.XPATH, "//*[normalize-space()='Your Cart']")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#checkout, [data-test='checkout']")),
                ))
            else:
                raise

    def sort_by(self, value):
        select_element = self.wait.until(EC.visibility_of_element_located(self.SORT_SELECT))
        Select(select_element).select_by_value(value)
        self.wait.until(lambda _driver: Select(self.driver.find_element(*self.SORT_SELECT)).first_selected_option.get_attribute("value") == value)

    def get_prices(self):
        elements = self.wait.until(lambda driver: driver.find_elements(*self.ITEM_PRICES))
        return [float(element.text.replace("$", "").strip()) for element in elements]

    def get_product_names(self):
        elements = self.wait.until(lambda driver: driver.find_elements(*self.ITEM_NAMES))
        return [element.text.strip() for element in elements]

    def logout(self):
        menu = self.wait.until(EC.presence_of_element_located(self.MENU_BUTTON))
        self.driver.execute_script("arguments[0].click();", menu)

        logout_link = self.wait.until(EC.presence_of_element_located(self.LOGOUT_LINK))
        href = logout_link.get_attribute("href")
        self.driver.execute_script("arguments[0].click();", logout_link)

        try:
            self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
        except Exception:
            if href:
                self.driver.get(href)
            else:
                self.driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
                self.driver.delete_all_cookies()
                self.driver.get("https://www.saucedemo.com/")
            self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))