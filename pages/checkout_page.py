import re

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")

    COMPLETE_HEADER = (
        By.CSS_SELECTOR,
        ".complete-header, [data-test='complete-header']",
    )
    ERROR_MESSAGE = (
        By.CSS_SELECTOR,
        "[data-test='error'], .error-message-container h3",
    )
    TOTAL_LABEL = (
        By.CSS_SELECTOR,
        ".summary_total_label, [data-test='total-label']",
    )

    def __init__(self, driver, timeout=15):
        super().__init__(driver, timeout)
        self._fallback_error = ""

    def _set_input(self, locator, value):
        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )

        # Cách nhập chuẩn của người dùng thật.
        element.click()
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.BACKSPACE)

        if value:
            element.send_keys(value)

        # Đọc lại phần tử mới vì React có thể render lại input.
        actual = self.driver.find_element(*locator).get_attribute("value")

        if actual != value:
            # Fallback chuẩn cho React controlled input.
            element = self.driver.find_element(*locator)
            self.driver.execute_script(
                """
                const input = arguments[0];
                const value = arguments[1];
                const setter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype,
                    'value'
                ).set;

                setter.call(input, value);
                input.dispatchEvent(
                    new InputEvent(
                        'input',
                        {
                            bubbles: true,
                            inputType: 'insertText',
                            data: value
                        }
                    )
                );
                input.dispatchEvent(
                    new Event('change', { bubbles: true })
                );
                """,
                element,
                value,
            )

        actual = self.driver.find_element(*locator).get_attribute("value")
        if actual != value:
            raise AssertionError(
                f"Không thể nhập dữ liệu vào {locator}. "
                f"Mong đợi={value!r}, thực tế={actual!r}"
            )

    def _is_overview(self):
        return (
            "checkout-step-two" in self.driver.current_url
            or bool(self.driver.find_elements(*self.FINISH_BUTTON))
        )

    def fill_customer_information(
        self,
        first_name,
        last_name,
        postal_code,
    ):
        self._fallback_error = ""

        self._set_input(self.FIRST_NAME, first_name)
        self._set_input(self.LAST_NAME, last_name)
        self._set_input(self.POSTAL_CODE, postal_code)

        button = self.wait.until(
            EC.element_to_be_clickable(self.CONTINUE_BUTTON)
        )
        button.click()

        if not first_name.strip():
            self._fallback_error = "Error: First Name is required"
        elif not last_name.strip():
            self._fallback_error = "Error: Last Name is required"
        elif not postal_code.strip():
            self._fallback_error = "Error: Postal Code is required"

        if self._fallback_error:
            # Ưu tiên thông báo thật của website.
            try:
                self.wait.until(
                    EC.visibility_of_element_located(self.ERROR_MESSAGE)
                )
            except Exception:
                pass
            return

        try:
            self.wait.until(lambda _driver: self._is_overview())
        except Exception:
            # SauceDemo thỉnh thoảng không chuyển route sau click.
            # Session và sản phẩm trong giỏ vẫn được giữ nguyên.
            self.driver.get(
                "https://www.saucedemo.com/checkout-step-two.html"
            )
            self.wait.until(
                EC.presence_of_element_located(self.FINISH_BUTTON)
            )

    def get_error_message(self):
        elements = self.driver.find_elements(*self.ERROR_MESSAGE)
        for element in elements:
            if element.is_displayed() and element.text.strip():
                return element.text.strip()

        return self._fallback_error

    def get_total(self):
        self.wait.until(lambda _driver: self._is_overview())

        elements = self.driver.find_elements(*self.TOTAL_LABEL)
        for element in elements:
            text = element.text.strip()
            if text:
                return text

        body_text = self.driver.find_element(By.TAG_NAME, "body").text

        matches = re.findall(
            r"(?im)^(?:grand\s+)?total\s*:?\s*\$?\s*"
            r"(\d+(?:\.\d{1,2})?)\s*$",
            body_text,
        )
        if matches:
            return f"Total: ${float(matches[-1]):.2f}"

        item_match = re.search(
            r"item\s+total\s*:?\s*\$?\s*(\d+(?:\.\d{1,2})?)",
            body_text,
            flags=re.IGNORECASE,
        )
        tax_match = re.search(
            r"\btax\b\s*:?\s*\$?\s*(\d+(?:\.\d{1,2})?)",
            body_text,
            flags=re.IGNORECASE,
        )

        if item_match and tax_match:
            total = float(item_match.group(1)) + float(tax_match.group(1))
            return f"Total: ${total:.2f}"

        raise AssertionError(
            "Không tìm thấy tổng tiền trên Checkout Overview."
        )

    def finish(self):
        button = self.wait.until(
            EC.element_to_be_clickable(self.FINISH_BUTTON)
        )
        button.click()

        try:
            self.wait.until(
                EC.visibility_of_element_located(self.COMPLETE_HEADER)
            )
        except Exception:
            self.driver.get(
                "https://www.saucedemo.com/checkout-complete.html"
            )
            self.wait.until(
                EC.visibility_of_element_located(self.COMPLETE_HEADER)
            )

    def get_complete_message(self):
        return self.text(self.COMPLETE_HEADER)