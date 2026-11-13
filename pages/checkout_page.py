from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    # Bước 1: thông tin khách hàng
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # Bước 2: tổng quan đơn hàng
    ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price, [data-test='inventory-item-price']")
    ITEM_TOTAL_LABEL = (By.CSS_SELECTOR, ".summary_subtotal_label, [data-test='subtotal-label']")
    TAX_LABEL = (By.CSS_SELECTOR, ".summary_tax_label, [data-test='tax-label']")
    TOTAL_LABEL = (By.CSS_SELECTOR, ".summary_total_label, [data-test='total-label']")
    FINISH_BUTTON = (By.ID, "finish")

    # Bước 3: hoàn tất
    COMPLETE_HEADER = (By.CSS_SELECTOR, ".complete-header, [data-test='complete-header']")

    def _set_input(self, locator, value):
        element = self.find_clickable(locator)
        element.click()
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.BACKSPACE)
        if value:
            element.send_keys(value)

        # SauceDemo dùng React: đôi khi ô đã hiện chữ nhưng state của React chưa cập nhật.
        # Đọc lại giá trị; nếu chưa đúng thì gán bằng setter gốc và phát sự kiện input/change.
        if self.driver.find_element(*locator).get_attribute("value") != value:
            self.driver.execute_script(
                """
                const input = arguments[0];
                const setter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value'
                ).set;
                setter.call(input, arguments[1]);
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
                """,
                self.driver.find_element(*locator),
                value,
            )

        actual = self.driver.find_element(*locator).get_attribute("value")
        if actual != value:
            raise AssertionError(f"Could not type into {locator}: expected {value!r}, got {actual!r}")

    def fill_customer_information(self, first_name, last_name, postal_code):
        self._set_input(self.FIRST_NAME, first_name)
        self._set_input(self.LAST_NAME, last_name)
        self._set_input(self.POSTAL_CODE, postal_code)
        self.find_clickable(self.CONTINUE_BUTTON).click()


    def get_error_message(self):
        # Chờ lỗi thật trên trang. Nếu trang không hiện lỗi, test sẽ fail (TimeoutException).
        return self.text(self.ERROR_MESSAGE)

    def _read_amount(self, locator):
        # "Item total: $29.99" -> 29.99
        return float(self.text(locator).split("$")[-1])

    def get_item_prices(self):
        self.find_visible(self.FINISH_BUTTON)
        return [float(e.text.replace("$", "").strip()) for e in self.find_all(self.ITEM_PRICES)]

    def get_item_total(self):
        return self._read_amount(self.ITEM_TOTAL_LABEL)

    def get_tax(self):
        return self._read_amount(self.TAX_LABEL)

    def get_total(self):
        return self._read_amount(self.TOTAL_LABEL)

    def finish(self):
        self.click(self.FINISH_BUTTON)
        self.find_visible(self.COMPLETE_HEADER)

    def get_complete_message(self):
        return self.text(self.COMPLETE_HEADER)
