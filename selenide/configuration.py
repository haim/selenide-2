from dataclasses import dataclass

from selenium import webdriver


@dataclass
class Config:
    driver: webdriver
    mode: str
    timeout: int
    url: str
    width: int
    height: int
