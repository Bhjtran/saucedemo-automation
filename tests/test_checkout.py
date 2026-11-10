import pytest
from config import BASE_URL, STANDARD_USER, PASSWORD
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.mark.smoke
def test_complete_checkout(driver):
    login = LoginPage(driver)
    inventory = InventoryPage(driver)
    cart = CartPage(driver)
    checkout = CheckoutPage(driver)

    login.open(BASE_URL)
    login.login(STANDARD_USER, PASSWORD)
    inventory.add_product("sauce-labs-backpack")
    inventory.open_cart()
    cart.checkout()

    checkout.fill_customer_information("Pham", "Tran", "700000")
    assert "Total:" in checkout.get_total()

    checkout.finish()
    assert checkout.get_complete_message() == "Thank you for your order!"


@pytest.mark.negative
def test_checkout_missing_first_name(driver):
    login = LoginPage(driver)
    inventory = InventoryPage(driver)
    cart = CartPage(driver)
    checkout = CheckoutPage(driver)

    login.open(BASE_URL)
    login.login(STANDARD_USER, PASSWORD)
    inventory.add_product("sauce-labs-backpack")
    inventory.open_cart()
    cart.checkout()

    checkout.fill_customer_information("", "Tran", "700000")
    assert "First Name is required" in checkout.get_error_message()
