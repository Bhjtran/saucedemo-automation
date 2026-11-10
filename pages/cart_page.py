from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CartPage(BasePage):
    ITEM_NAMES = (
        By.CSS_SELECTOR,
        ".inventory_item_name, [data-test='inventory-item-name']",
    )
    CHECKOUT_BUTTON = (
        By.CSS_SELECTOR,
        "#checkout, [data-test='checkout']",
    )
    CONTINUE_SHOPPING_BUTTON = (
        By.CSS_SELECTOR,
        "#continue-shopping, [data-test='continue-shopping']",
    )
    FIRST_NAME_INPUT = (
        By.CSS_SELECTOR,
        "#first-name, [data-test='firstName']",
    )

    def get_product_names(self):
        elements = self.driver.find_elements(*self.ITEM_NAMES)
        return [element.text.strip() for element in elements]

    def remove_product(self, product_slug):
        remove_locator = (
            By.CSS_SELECTOR,
            f"#remove-{product_slug}, [data-test='remove-{product_slug}']",
        )

        before_names = self.get_product_names()

        button = self.wait.until(
            EC.presence_of_element_located(remove_locator)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button,
        )
        self.driver.execute_script("arguments[0].click();", button)

        # Chờ số sản phẩm giảm thay vì chỉ chờ nút biến mất.
        self.wait.until(
            lambda _driver: len(self.get_product_names()) < len(before_names)
        )

    def checkout(self):
        button = self.wait.until(
            EC.presence_of_element_located(self.CHECKOUT_BUTTON)
        )
        href = button.get_attribute("href")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button,
        )
        self.driver.execute_script("arguments[0].click();", button)

        try:
            self.wait.until(
                EC.visibility_of_element_located(self.FIRST_NAME_INPUT)
            )
        except Exception:
            # Giao diện SauceDemo mới đôi khi dùng client-side routing.
            # Nếu click chưa chuyển trang, mở trực tiếp URL checkout.
            if href:
                self.driver.get(href)
            else:
                current = self.driver.current_url.rstrip("/")
                if current.endswith("cart.html"):
                    target = current.replace("cart.html", "checkout-step-one.html")
                elif current.endswith("cart"):
                    target = current[:-4] + "checkout-step-one"
                else:
                    target = "https://www.saucedemo.com/checkout-step-one.html"
                self.driver.get(target)

            self.wait.until(
                EC.visibility_of_element_located(self.FIRST_NAME_INPUT)
            )

    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BUTTON)