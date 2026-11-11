import logging
from pathlib import Path

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import DEFAULT_TIMEOUT

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(
            driver,
            timeout,
            ignored_exceptions=(StaleElementReferenceException,),
        )

    def open(self, url):
        self.driver.get(url)

    def find_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def click(self, locator):
        element = self.find_clickable(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            element,
        )

        # Ưu tiên click thật. Chỉ dùng cách khác khi bị che hoặc không tương tác được,
        # và ghi log để biết lần click đó không giống người dùng thật.
        try:
            element.click()
        except (ElementClickInterceptedException, ElementNotInteractableException):
            logger.warning("Normal click failed on %s, trying ActionChains", locator)
            try:
                ActionChains(self.driver).move_to_element(element).click().perform()
            except (ElementClickInterceptedException, ElementNotInteractableException):
                logger.warning("ActionChains click failed on %s, using JavaScript click", locator)
                self.driver.execute_script("arguments[0].click();", element)

        return element

    def type(self, locator, value):
        element = self.find_visible(locator)
        element.clear()
        element.send_keys(value)

    def text(self, locator):
        return self.find_visible(locator).text

    def wait_url_contains(self, value):
        return self.wait.until(EC.url_contains(value))

    def screenshot(self, name):
        folder = Path("screenshots")
        folder.mkdir(exist_ok=True)
        self.driver.save_screenshot(str(folder / name))
