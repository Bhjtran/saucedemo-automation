import pytest
from config import BASE_URL, STANDARD_USER, PASSWORD
from pages.login_page import LoginPage


@pytest.mark.smoke
def test_login_successfully(driver):
    page = LoginPage(driver)
    page.open(BASE_URL)
    page.login(STANDARD_USER, PASSWORD)

    assert "inventory.html" in driver.current_url


@pytest.mark.negative
@pytest.mark.parametrize(
    "username,password,expected_text",
    [
        ("standard_user", "wrong_password", "Username and password do not match"),
        ("", PASSWORD, "Username is required"),
        (STANDARD_USER, "", "Password is required"),
    ],
)
def test_login_with_invalid_data(driver, username, password, expected_text):
    page = LoginPage(driver)
    page.open(BASE_URL)
    page.login(username, password)

    assert expected_text in page.get_error_message()
