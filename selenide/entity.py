from __future__ import annotations

import time
from typing import Union, Tuple

import allure
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException,
    NoSuchElementException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from selenide.selectors import by_text

cf = None


def by2locator(describe, location) -> Tuple:
    """根据入参定位描述判断元素定位条件支持三大类定位方式
    1.默认SELENIUM TUPLE(By.XX, XX)
    2.直接css 或者 xpath
    3.元素text
    :param describe: 固定描述
    :param location: 定位描述
    :return: 元组形式标准SELENIUM可识别定位信息
    """
    if isinstance(location, tuple):
        # 默认遵循标准SELENIUM识别定位信息
        return location
    elif isinstance(location, str):
        starts = location.startswith
        if any((starts(maker) for maker in ("/", "./", "..", "("))):
            return By.XPATH, location
        else:
            return By.CSS_SELECTOR, location
    # 如果只输入了元素描述则根据描述文本信息查找元素
    elif not location and describe:
        return By.XPATH, by_text(describe)
    raise TypeError


class Element:
    # 当前不支持子类查找，需要的话可以使用css的子类元素查找方式支持
    # 最佳推荐除过可唯一标识属性外使用css来定位元素
    def __init__(
        self, describe: str = None, locator: Union[str, tuple] = None
    ):  # noqa
        self.describe = describe
        self.locator = by2locator(describe, locator)

    def __get__(self, instance, owner):
        if not instance:
            raise PermissionError("Element should be in page.")
        cf.DRIVER = instance.driver
        return self

    def __set__(self, instance, value):
        self.__get__(instance, instance.__class__)
        try:
            # Element("describe", "#username") = awesome
            self.input(value)
        except WebDriverException:
            raise PermissionError("Element should be support input.")

    @property
    def driver(self):
        return cf.DRIVER

    def locate(self, condition):
        # 一般情况下为了元素上的操作而查找元素，默认通过指定状态显示等待条件
        # 如果仅需要判断元素状态 if Element("describe", "#username").present
        try:
            # TMS 产品页面加载项
            WebDriverWait(self.driver, cf.POLL_TIMEOUT).until_not(
                ec.presence_of_element_located(
                    ("css selector", ".c7n-spin-initial-dot")
                )  # noqa
            )

            element = WebDriverWait(self.driver, cf.POLL_TIMEOUT).until(
                condition
            )  # noqa
            if not isinstance(element, list):
                self.driver.execute_script(
                    "arguments[0].scrollIntoViewIfNeeded(true);", element
                )  # noqa
                time.sleep(0.5)
                self.driver.execute_script(
                    'arguments[0].style.border="2px solid red";', element
                )  # noqa
                time.sleep(0.5)
                self.driver.execute_script(
                    'arguments[0].style.border="";', element
                )  # noqa
            element = WebDriverWait(self.driver, cf.POLL_TIMEOUT).until(
                condition
            )  # noqa
        except TimeoutException:
            raise NoSuchElementException(
                f"Describe: {self.describe} Locator: {self.locator}"
            )  # noqa
        return element

    @property
    def present(self):
        with allure.step(f"Assert {self.describe} present."):
            return self.locate(ec.presence_of_element_located(self.locator))

    @property
    def staleness(self):
        with allure.step(f"Assert {self.describe} staleness."):
            return self.locate(ec.staleness_of(self.locator))

    @property
    def visible(self):
        with allure.step(f"Assert {self.describe} visible."):
            return self.locate(ec.visibility_of_element_located(self.locator))

    @property
    def invisible(self):
        with allure.step(f"Assert {self.describe} invisible."):
            return self.locate(
                ec.invisibility_of_element_located(self.locator)
            )  # noqa

    @property
    def clickable(self):
        with allure.step(f"Assert {self.describe} clickable."):
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
        with allure.step(f"获取 {self.describe} text"):
            return self.present.text

    @property
    def value(self):
        with allure.step(f"获取 {self.describe} value"):
            return self.present.get_attribute("value")

    def attr(self, name):
        with allure.step(f"获取 {self.describe} {name}"):
            return self.present.get_attribute(name)

    def set_value(self, value):
        with allure.step(f"设置 {self.describe} value = {value}"):
            set_value_js = f"arguments[0].setAttribute('value','{value}')"
            self.driver.execute_script(set_value_js, self.visible)
        return self

    def set_attr(self, name, value):
        with allure.step(f"设置 {self.describe} 属性: {name} = {value}"):
            set_attr_js = f"arguments[0].setAttribute('{name}','{value}')"
            self.driver.execute_script(set_attr_js, self.present)
        return self

    def input(self, value):
        with allure.step(f"输入 {self.describe} = {value}"):
            element = self.visible
            element.clear()
            element.send_keys(value)
        return self

    def input_by_js(self, value):
        with allure.step(f"输入 {self.describe} = {value}"):
            input_js = f'arguments[0].value="{value}"'
            self.driver.executeScript(input_js, self.visible)
        return self

    def click(self):
        with allure.step(f"点击 {self.describe}"):
            self.clickable.click()
        return self

    def click_by_js(self):
        with allure.step(f"点击 {self.describe}"):
            self.driver.executeScript("arguments[0].click()", self.visible)
        return self

    def hover(self):
        with allure.step(f"悬浮 {self.describe}"):
            action = ActionChains(self.driver)
            action.move_to_element(self.present).perform()
        return self

    def double_click(self):
        with allure.step(f"双击 {self.describe}"):
            action = ActionChains(self.driver)
            action.double_click(self.present).perform()
        return self

    def context_click(self):
        with allure.step(f"右击 {self.describe}"):
            action = ActionChains(self.driver)
            action.context_click(self.present).perform()
        return self

    def hold_click(self):
        with allure.step(f"悬浮后点击 {self.describe}"):
            action = ActionChains(self.driver)
            action.click_and_hold(self.present).perform()
        return self

    def drag_and_drop(self, target: Element):
        with allure.step(f"拖拽 {self.describe} 至 {target.describe}"):
            action = ActionChains(self.driver)
            action.drag_and_drop(self.present, target).perform()
        return target

    def enter(self):
        with allure.step("点击 回车"):
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        return self

    def tab(self):
        with allure.step("点击 TAB键"):
            ActionChains(self.driver).send_keys(Keys.TAB).perform()
        return self

    def switch2frame(self):
        with allure.step(f"切换至 {self.describe}"):
            frame = ec.frame_to_be_available_and_switch_to_it
            self.locate(frame(self.locator))
        return self


class Collection(Element):
    """原生WebElement容器"""

    @property
    def present(self):
        all_presence = ec.presence_of_all_elements_located
        return self.locate(all_presence(self.locator))

    @property
    def visible(self):
        all_visibility = ec.visibility_of_all_elements_located
        return self.locate(all_visibility(self.locator))

    @property
    def first(self):
        return self.present[0]

    @property
    def last(self):
        return self.present[-1]

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
