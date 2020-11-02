from __future__ import annotations

import time
from typing import Optional, Union

import allure
from selenium.common.exceptions import (
    InvalidElementStateException,
    WebDriverException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from selenide.configuration import Config
from selenide.helper import element_mark, to_by


class Element:
    def __init__(self, describe: Optional[str], locator: Union[str, tuple]):
        self.describe = describe
        self.locator = to_by(locator)
        self.action = ActionChains(self.driver)

    def __get__(self, instance, owner):
        if not instance:
            raise PermissionError("Element should be in page.")
        self.driver = instance.driver
        return self

    def __set__(self, instance, value):
        self.__get__(instance, instance.__class__)
        try:
            self.input(value)
        except WebDriverException:
            raise PermissionError("Element should be support input.")

    def locate(self, condition):
        element = WebDriverWait(self.driver, Config.timeout).until(condition)
        with element_mark(self.driver, element):
            time.sleep(0.5)
        return element

    @property
    def present(self):
        return self.locate(ec.presence_of_element_located(self.locator))

    @property
    def staleness(self):
        return self.locate(ec.staleness_of(self.locator))

    @property
    def visible(self):
        return self.locate(ec.visibility_of_element_located(self.locator))

    @property
    def invisible(self):
        return self.locate(ec.invisibility_of_element_located(self.locator))

    @property
    def clickable(self):
        return self.locate(ec.element_to_be_clickable(self.locator))

    def has_text(self, text):
        with allure.step(f"Assert {self.describe} has text = {text}"):
            present = ec.text_to_be_present_in_element
            return self.locate(present(self.locator, text))

    def has_attr(self, name, value):
        with allure.step(f"Assert {self.describe} has {name} = {value}"):
            return value == self.present.get_attribute(name)

    @property
    def text(self):
        with allure.step(f"Get {self.describe} text"):
            return self.present.text

    @property
    def value(self):
        with allure.step(f"Get {self.describe} value"):
            return self.present.get_attribute("value")

    def attr(self, name):
        with allure.step(f"Get {self.describe} {name}"):
            return self.present.get_attribute(name)

    def set_value(self, value):
        with allure.step(f"Set {self.describe} value = {value}"):
            set_value_js = f"arguments[0].setAttribute('value','{value}')"
            self.driver.execute_script(set_value_js, self.visible)
        return self

    def set_attr(self, name, value):
        with allure.step(f"Set {self.describe} attribute: {name} = {value}"):
            set_attr_js = f"arguments[0].setAttribute('{name}','{value}')"
            self.driver.execute_script(set_attr_js, self.present)
        return self

    def input(self, value):
        with allure.step(f"Input {value} on {self.describe}"):
            self.visible.clear()
            self.visible.send_keys(value)
        return self

    def input_by_js(self, value):
        with allure.step(f"Input {value} on {self.describe}"):
            input_js = f'arguments[0].value="{value}"'
            self.driver.executeScript(input_js, self.visible)
        return self

    def click(self):
        with allure.step(f"Click Element {self.describe}"):
            self.clickable.click()
        return self

    def click_by_js(self):
        with allure.step(f"Click Element {self.describe}"):
            self.driver.executeScript("arguments[0].click()", self.visible)
        return self

    def hover(self):
        with allure.step(f"Hover Element {self.describe}"):
            self.action.move_to_element(self.visible).perform()
        return self

    def double_click(self):
        with allure.step(f"Double click Element {self.describe}"):
            self.action.double_click(self.visible).perform()
        return self

    def context_click(self):
        with allure.step(f"Right click Element {self.describe}"):
            self.action.context_click(self.visible).perform()
        return self

    def hold_click(self):
        with allure.step(f"Hold click Element {self.describe}"):
            self.action.click_and_hold(self.visible).perform()
        return self

    def drag_and_drop(self, target: Element):
        with allure.step(f"Drag {self.describe} drop {target.describe}"):
            self.action.drag_and_drop(self.visible, target).perform()
        return target

    def enter(self):
        with allure.step("Press ENTER"):
            try:
                self.present.send_keys(Keys.ENTER)
            except InvalidElementStateException:
                self.input(Keys.ENTER)
        return self

    def tab(self):
        with allure.step("Press TAB"):
            try:
                self.present.send_keys(Keys.TAB)
            except InvalidElementStateException:
                self.input(Keys.TAB)
        return self

    def switch2frame(self):
        with allure.step(f"Switch to {self.describe}"):
            frame = ec.frame_to_be_available_and_switch_to_it
            self.locate(frame(self.locator))
        return self


class Collection(Element):
    @property
    def present(self):
        all_presence = ec.presence_of_all_elements_located
        return self.locate(all_presence(self.locator))

    @property
    def visible(self):
        all_visibility = ec.visibility_of_all_elements_located
        return self.locate(all_visibility(self.locator))

    @property
    def empty(self) -> bool:
        return self.present

    @property
    def size(self) -> int:
        return len(self.present)

    def size_equal(self, size: int) -> bool:
        return size == self.size

    def size_greater(self, size: int) -> bool:
        return size > self.size

    def size_less(self, size: int) -> bool:
        return size < self.size

    def size_not_equal(self, size: int) -> bool:
        return size != self.size
