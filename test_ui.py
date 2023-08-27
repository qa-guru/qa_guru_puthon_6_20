from time import sleep

import requests
from allure import step
from selene.support.conditions import have
from selene.support.shared import browser


LOGIN = "example1200@example.com"
PASSWORD = "123456"
WEB_URL = "https://demowebshop.tricentis.com/"
API_URL = "https://demowebshop.tricentis.com/"

def test_login():
    """Successful authorization to some demowebshop (UI)"""
    with step("Open login page"):
        browser.open("http://demowebshop.tricentis.com/login")

    with step("Fill login form"):
        browser.element("#Email").send_keys(LOGIN)
        browser.element("#Password").send_keys(PASSWORD).press_enter()

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


def test_login_through_api():
    """Successful authorization to some demowebshop (UI)"""
    with step("Get auth cookie though API"):
        url = API_URL + "/login"
        auth_cookie_name = "NOPCOMMERCE.AUTH"
        payload = {
            'Email': LOGIN,
            "Password": PASSWORD,
            "RememberMe": False
        }
        response = requests.request("POST", url, data=payload, allow_redirects=False)
        cookie = response.cookies.get(auth_cookie_name)

    with step("Open browser with auth cookie"):
        browser.open(WEB_URL)
        browser.driver.add_cookie({"name": auth_cookie_name, "value": cookie})
        browser.open(WEB_URL)

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))
