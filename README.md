# selenide
> Realization of UI automated testing wheels by selenium+allure.

```python
from selenium import webdriver

from selenide.element import Element
from selenide.page import Page


class LoginPage(Page):
    search = Element("input", "#kw")
    search_btn = Element("search", "#su")

    def login(self):
        self.driver.get("https://www.baidu.com/")
        self.search.input("50331812").enter()
        self.search_btn.click()


def test_login():
    browser = webdriver.Chrome("chromedriver.exe")
    LoginPage(browser).login()
    assert browser.title == "expect value"

```
