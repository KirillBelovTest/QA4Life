from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import abc
from abc import abstractmethod

from rzd.elements import Button, Input
from rzd.decorators import input_field


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.waiter = WebDriverWait(driver, 10)

    def open(self, url: str):
        self.driver.get(url)


class RZDMainPage(BasePage):
    def open(self):
        super().open("https://www.rzd.ru/")

    @property
    def button_login(self) -> Button:
        return Button(self.driver, (By.XPATH, "//*[@data-test-id='profile']//span[text()='Вход']"), self.waiter)

    @property
    def form_login(self) -> LoginForm:
        return LoginForm(self)


class BaseLoginElement(abc.ABC):
    def __init__(self, page: BasePage):
        self.page = page

    @property
    @abstractmethod
    def input_login_in_form(self) -> Input: pass

    @property
    @abstractmethod
    def input_password_in_form(self) -> Input: pass

    @property
    @abstractmethod
    def button_submit(self) -> Button: pass

    def login(self, username: str, password: str):
        self.input_login_in_form.send_keys(username)
        self.input_password_in_form.send_keys(password)
        self.button_submit.click()


@container_locator(xpath="//form[@data-id='login']")
class LoginForm(BaseLoginElement):
    @property
    def input_login_in_form(self) -> Input:
        return Input(self.page.driver, (By.XPATH, "//input[@placeholder='Логин']"), self.page.waiter)

    @property
    def input_password_in_form(self) -> Input:
        return Input(self.page.driver, (By.XPATH, "//input[@placeholder='Пароль']"), self.page.waiter)

    @property
    def button_submit(self) -> Button:
        return Button(self.page.driver, (By.XPATH, "//button[@type='submit']"), self.page.waiter)


class LoginSideBar(BaseLoginElement):
    @property
    def input_login_in_form(self) -> Input:
        return Input(self.page.driver, (By.XPATH, "//*[@formcontrolname='login']//input"), self.page.waiter)

    @property
    def input_password_in_form(self) -> Input:
        return Input(self.page.driver, (By.XPATH, "//*[@formcontrolname='password']//input"), self.page.waiter)

    @property
    def button_submit(self) -> Button:
        return Button(self.page.driver, (By.XPATH, "//button[@type='submit']"), self.page.waiter)


class RZDVacancies(BasePage):
    def open(self):
        return super().open('https://team.rzd.ru/career/vacancies')

    @input_field(xpath="//input[@class='ui-input__field']")
    def input_search_vac(self) -> Input: pass