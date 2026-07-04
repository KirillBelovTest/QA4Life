from playwright.sync_api import Page, sync_playwright
from time import sleep


def example():
    with sync_playwright() as manager:
        browser = manager.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://react-shopping-cart-67954.firebaseapp.com")
        sleep(15)
        browser.close()


def test_1(page):
    page.goto("https://react-shopping-cart-67954.firebaseapp.com")
    sleep(1)

import re
from playwright.sync_api import Playwright, sync_playwright, expect


def test_2(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://react-shopping-cart-67954.firebaseapp.com/")
    page.get_by_text("XL", exact=True).click()
    page.get_by_role("button", name="Add to cart").nth(5).click()
    page.get_by_role("button", name="+").click()
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_role("button", name="Checkout").click()

    sleep(5)

    # ---------------------
    context.close()
    browser.close()


class ReactShoppingCartPage:
    def __init__(self, page: Page):
        self.cart = page.locator("//div[@titile='Products in cart quantity']")
        self.lc1 = page.locator("[attribute]")
        self.checkut = page.get_by_role("button", text="Checkout")