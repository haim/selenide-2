from selenium.webdriver.remote.webdriver import WebDriver


class Config:
    driver: WebDriver
    mode: str
    timeout: int = 6
    url: str
    width: int
    height: int
