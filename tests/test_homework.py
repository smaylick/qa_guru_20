import logging
import allure
from selene import browser, have, be
from allure_commons._allure import step

from tests.conftest import LOGIN, PASSWORD, BASE_URL
from utils.utils import post_request


@allure.title("Проверка успешной авторизации")
def test_successful_authorization_with_cookie():
    response = post_request("/login", data={"Email": LOGIN, "Password": PASSWORD}, allow_redirects=False)
    cookie = response.cookies.get("NOPCOMMERCE.AUTH")
    logging.info(cookie)
    with step("Открытие главной страницы пользователем и проверка успешной авторизации"):
        browser.open(BASE_URL)
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open(BASE_URL)
        browser.element(".account").should(have.text(LOGIN))


@allure.title("Проверка добавления товара в корзину")
def test_add_item_to_cart_with_api():
    response = post_request("/login", data={"Email": LOGIN, "Password": PASSWORD}, allow_redirects=False)
    cookie = response.cookies.get("NOPCOMMERCE.AUTH")
    browser.open(BASE_URL)
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
    with step("Добавляем товар в корзину"):
        post_request("/addproducttocart/details/74/1", data={
            "product_attribute_74_5_26": 81,
            "product_attribute_74_6_27": 83,
            "product_attribute_74_3_28": 86,
            "addtocart_74.EnteredQuantity": 1
        })
    with step("Проверяем наличие товара в корзине"):
        browser.open(f"{BASE_URL}/cart")
        browser.element('[href*="3871103"]').should(be.visible)
