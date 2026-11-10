"""Chạy demo luồng end-to-end không cần pytest."""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import BASE_URL, STANDARD_USER, PASSWORD
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def run_demo():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        login = LoginPage(driver)
        inventory = InventoryPage(driver)
        cart = CartPage(driver)
        checkout = CheckoutPage(driver)

        print("1. Mở trang và đăng nhập")
        login.open(BASE_URL)
        login.login(STANDARD_USER, PASSWORD)
        inventory.wait_url_contains("inventory.html")
        inventory.screenshot("01_login_success.png")

        print("2. Thêm sản phẩm vào giỏ")
        inventory.add_product("sauce-labs-backpack")
        assert inventory.get_cart_count() == 1
        inventory.screenshot("02_added_product.png")

        print("3. Kiểm tra giỏ hàng")
        inventory.open_cart()
        assert "Sauce Labs Backpack" in cart.get_product_names()
        cart.screenshot("03_cart.png")

        print("4. Thanh toán")
        cart.checkout()
        checkout.fill_customer_information("Pham", "Tran", "700000")
        checkout.screenshot("04_checkout_overview.png")
        checkout.finish()

        assert checkout.get_complete_message() == "Thank you for your order!"
        checkout.screenshot("05_checkout_complete.png")
        print("✅ Toàn bộ luồng end-to-end đã PASS")
    except Exception as exc:
        driver.save_screenshot("screenshots/FAILED_demo.png")
        print(f"❌ TEST FAIL: {exc}")
        raise
    finally:
        driver.quit()


if __name__ == "__main__":
    run_demo()
