import contextlib
import time
from typing import Tuple, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


@contextlib.contextmanager
def element_mark(driver: WebDriver, element: Union[WebElement, bool]):
    if isinstance(element, WebElement):
        driver.execute_script(
            "arguments[0].scrollIntoViewIfNeeded(true);", element)
        time.sleep(0.5)
        mark_red = 'arguments[0].style.border="2px solid #FF0000"'
        mark_nul = 'arguments[0].style.border=""'
        driver.execute_script(mark_red, element)
        yield
        driver.execute_script(mark_nul, element)


def to_by(location: Union[str, tuple]) -> Tuple[str, str]:
    if isinstance(location, tuple):
        return location
    elif isinstance(location, str):
        if any((location.startswith(marker)
                for marker in ('/', './', '..', '('))):
            return By.XPATH, location
        else:
            return By.CSS_SELECTOR, location
    raise TypeError
