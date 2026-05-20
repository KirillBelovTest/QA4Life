import time

from selenium import webdriver

from rzd.pages import RZDMainPage, RZDVacancies

def test_search():
    driver = webdriver.Chrome()
    page = RZDMainPage(driver)

    page.open()
    page.button_login.click()
    page.form_login.login("kirillbelovtest", "qwerty12345")

    time.sleep(10)

    vacpage = RZDVacancies(driver)
    vacpage.open()
    vacpage.input_search_vac.send_keys('Автотестировщик')

    time.sleep(10)