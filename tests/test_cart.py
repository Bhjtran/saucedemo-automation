import pytest
from config import BASE_URL, STANDARD_USER, PASSWORD
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


def login_standard_user(driver):
    login = LoginPage(driver)
    login.open(BASE_URL)
    login.login(STANDARD_USER, PASSWORD)
    login.wait_url_contains("inventory")


@pytest.mark.smoke
def test_add_product_to_cart(driver):
    login_standard_user(driver)
    inventory = InventoryPage(driver)
    cart = CartPage(driver)

    inventory.add_product("sauce-labs-backpack")
    assert inventory.get_cart_count() == 1

    inventory.open_cart()
    assert "Sauce Labs Backpack" in cart.get_product_names()


def test_add_two_products_and_remove_one(driver):
    login_standard_user(driver)
    inventory = InventoryPage(driver)
    cart = CartPage(driver)

    inventory.add_product("sauce-labs-backpack")
    inventory.add_product("sauce-labs-bike-light")
    assert inventory.get_cart_count() == 2

    inventory.remove_product("sauce-labs-bike-light")
    assert inventory.get_cart_count() == 1

    inventory.open_cart()
    assert cart.get_product_names() == ["Sauce Labs Backpack"]


def test_remove_product_from_cart(driver):
    login_standard_user(driver)
    inventory = InventoryPage(driver)
    cart = CartPage(driver)

    inventory.add_backpack()
    inventory.open_cart()
    assert "Sauce Labs Backpack" in cart.get_product_names()

    cart.remove_product("sauce-labs-backpack")
    assert cart.get_product_names() == []
