from config import BASE_URL, STANDARD_USER, PASSWORD
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


def test_sort_price_low_to_high(driver):
    login = LoginPage(driver)
    inventory = InventoryPage(driver)

    login.open(BASE_URL)
    login.login(STANDARD_USER, PASSWORD)
    inventory.sort_by("lohi")

    prices = inventory.get_prices()
    assert prices == sorted(prices)


def test_sort_name_z_to_a(driver):
    login = LoginPage(driver)
    inventory = InventoryPage(driver)

    login.open(BASE_URL)
    login.login(STANDARD_USER, PASSWORD)
    inventory.sort_by("za")

    names = inventory.get_product_names()
    assert names == sorted(names, reverse=True)
