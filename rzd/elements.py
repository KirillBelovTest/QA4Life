from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


class BaseElement:
    def __init__(self, driver: WebDriver, locator: By, waiter: WebDriverWait, index: Optional[int] = None):
        self.driver = driver
        self.locator = locator
        self.waiter = waiter
        self.index = index

    def find(self) -> Optional[WebElement]:
        if self.index is not None:
            elements = self.waiter.until(lambda driver: driver.find_elements(*self.locator))
            if len(elements) > self.index:
                return elements[self.index]
            return None
        return self.waiter.until(lambda driver: driver.find_element(*self.locator))


class Button(BaseElement):
    def click(self):
        element = self.find()
        if element:
            element.click()


class Input(BaseElement):
    def send_keys(self, keys: str):
        element = self.find()
        if element:
            element.clear()
            element.send_keys(keys)

    def get_value(self) -> str:
        element = self.find()
        return element.get_attribute('value') if element else ""


class Label(BaseElement):
    def get_text(self) -> str:
        element = self.find()
        return element.text if element else ""