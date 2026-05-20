from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from typing import List, Optional, Callable, Any
from functools import wraps

from rzd.elements import Button, Input, Label


def _get_element(driver: WebDriver, locator: tuple, waiter: WebDriverWait, element_class):
    return element_class(driver, locator, waiter)


def _get_elements(driver: WebDriver, locator: tuple, waiter: WebDriverWait, element_class) -> List:
    try:
        elements = driver.find_elements(*locator)
        return [element_class(driver, (locator[0], locator[1], i), waiter) for i, _ in enumerate(elements)]
    except:
        return []


def button(xpath: str):
    def decorator(func: Callable) -> property:
        @property
        @wraps(func)
        def wrapper(self):
            return _get_element(
                self.driver,
                (By.XPATH, xpath),
                self.waiter,
                Button
            )
        return wrapper
    return decorator


def buttons(xpath: str):
    def decorator(func: Callable) -> property:
        @property
        @wraps(func)
        def wrapper(self):
            return _get_elements(
                self.driver,
                (By.XPATH, xpath),
                self.waiter,
                Button
            )
        return wrapper
    return decorator


def input_field(xpath: str):
    def decorator(func: Callable) -> property:
        @property
        @wraps(func)
        def wrapper(self):
            return _get_element(
                self.driver,
                (By.XPATH, xpath),
                self.waiter,
                Input
            )
        return wrapper
    return decorator


def input_fields(xpath: str):
    def decorator(func: Callable) -> property:
        @property
        @wraps(func)
        def wrapper(self):
            return _get_elements(
                self.driver,
                (By.XPATH, xpath),
                self.waiter,
                Input
            )
        return wrapper
    return decorator


def label(xpath: str):
    def decorator(func: Callable) -> property:
        @property
        @wraps(func)
        def wrapper(self):
            return _get_element(
                self.driver,
                (By.XPATH, xpath),
                self.waiter,
                Label
            )
        return wrapper
    return decorator


def labels(xpath: str):
    def decorator(func: Callable) -> property:
        @property
        @wraps(func)
        def wrapper(self):
            return _get_elements(
                self.driver,
                (By.XPATH, xpath),
                self.waiter,
                Label
            )
        return wrapper
    return decorator