# selenide
> Realization of UI automated testing wheels by selenium+allure.

```python
from selenium import webdriver

from src.element import Element
from src.page import Page


class LoginPage(Page):
    search = Element("百度一下", "#kw")
    search_btn = Element("搜索", "#su")

    def login(self):
        self.driver.get("https://www.baidu.com/")
        self.search.input("50331812").enter()
        self.search_btn.click()


def test_login():
    browser = webdriver.Chrome("chromedriver.exe")
    LoginPage(browser).login()
    assert browser.title == "百度一下，你就知道"

```
