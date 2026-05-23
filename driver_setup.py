"""
Создание браузера Chrome для тестов.

Selenium Manager (4.6+) сам подбирает chromedriver.
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

# Таймауты загрузки страницы (секунды)
PAGE_LOAD_TIMEOUT = 60
SCRIPT_TIMEOUT = 30


def create_chrome_driver() -> WebDriver:
    """Запускает Chrome с настройками для нестабильной сети."""
    options = Options()
    options.page_load_strategy = "eager"
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    driver.set_script_timeout(SCRIPT_TIMEOUT)
    return driver
