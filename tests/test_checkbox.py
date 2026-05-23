"""
Автотесты для страницы Check Box на demoqa.com.
"""

from __future__ import annotations

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from driver_setup import create_chrome_driver
from pages.checkbox_page import CheckboxPage


@pytest.fixture(scope="module")
def driver() -> WebDriver:
    """
    Один браузер на все тесты — меньше обращений к demoqa.com
    (снижает риск ERR_CONNECTION_RESET).
    """
    chrome = create_chrome_driver()
    yield chrome
    chrome.quit()


@pytest.fixture(scope="module")
def checkbox_page(driver: WebDriver) -> CheckboxPage:
    """Один раз открывает страницу Check Box для всех тестов."""
    return CheckboxPage(driver).open()


def test_select_home_checkbox(checkbox_page: CheckboxPage) -> None:
    """Выбор 'Home' и проверка, что чекбокс отмечен."""
    checkbox_page.click_checkbox("Home")

    assert checkbox_page.is_checkbox_selected("Home")
    assert "home" in checkbox_page.get_result_text().lower()


def test_expand_and_select_documents(checkbox_page: CheckboxPage) -> None:
    """Раскрытие дерева и выбор чекбокса 'Documents'."""
    checkbox_page.uncheck_all()
    checkbox_page.expand_node("Home")
    checkbox_page.set_checkbox("Documents", selected=True)

    assert checkbox_page.is_checkbox_selected("Documents"), (
        "Documents должен быть отмечен (aria-checked=true)"
    )
    assert checkbox_page.is_label_in_result("documents")


def test_toggle_checkbox_state(checkbox_page: CheckboxPage) -> None:
    """Повторный клик снимает выбор с чекбокса."""
    checkbox_page.uncheck_all()
    checkbox_page.expand_node("Home")

    checkbox_page.click_checkbox("Home")
    assert checkbox_page.is_checkbox_selected("Home")

    checkbox_page.click_checkbox("Home")
    assert not checkbox_page.is_checkbox_selected("Home")
