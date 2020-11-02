import time

from selenium.webdriver.remote.webdriver import WebDriver


class Page:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    @property
    def title(self):
        return self.driver.title

    @property
    def url(self):
        return self.driver.current_url

    def get(self, url: str):
        self.driver.get(url.strip())
        self.driver.maximize_window()

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()

    def refresh(self):
        self.driver.refresh()

    def execute_js(self, js):
        return self.driver.execute_script(js)

    @staticmethod
    def sleep(seconds):
        time.sleep(seconds)
