import time
from typing import Tuple, Union

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

_scroll2view = "arguments[0].scrollIntoViewIfNeeded(true)"
_marker = ("/", "./", "..", "(")


def mark(driver: webdriver, element: Union[WebElement, bool]):
    if isinstance(element, WebElement):
        driver.execute_script(_scroll2view, element)
        time.sleep(0.5)
        mark_red = 'arguments[0].style.border="2px solid #FF0000"'
        mark_nul = 'arguments[0].style.border=""'
        driver.execute_script(mark_red, element)
        time.sleep(0.5)
        driver.execute_script(mark_nul, element)
    return element


def to_by(describe, location) -> Tuple:
    if isinstance(location, tuple):
        return location
    elif isinstance(location, str):
        starts = location.startswith
        if any((starts(maker) for maker in _marker)):
            return By.XPATH, location
        else:
            return By.CSS_SELECTOR, location
    elif not location and describe:
        return By.XPATH, f"//*[text()={describe}]"
    raise TypeError
