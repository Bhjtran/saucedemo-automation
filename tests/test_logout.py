from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL, STANDARD_USER, PASSWORD
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


def test_logout(driver):
    login = LoginPage(driver)
    inventory = InventoryPage(driver)

    login.open(BASE_URL)
    login.login(STANDARD_USER, PASSWORD)
    inventory.wait_url_contains("inventory")
    inventory.logout()

    assert driver.current_url.rstrip("/") == BASE_URL.rstrip("/")
    assert inventory.wait.until(EC.visibility_of_element_located((By.ID, "login-button"))).is_displayed()
