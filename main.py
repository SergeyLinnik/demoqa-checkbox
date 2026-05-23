"""
Скрипт для ручного запуска: выбор чекбоксов на demoqa.com/checkbox
и проверка их состояния.

Запуск: python main.py
"""

from __future__ import annotations

from driver_setup import create_chrome_driver
from pages.checkbox_page import CheckboxPage


def run_checkbox_demo() -> None:
    """Демонстрация работы с чекбоксами на demoqa.com."""
    driver = create_chrome_driver()

    try:
        page = CheckboxPage(driver).open()

        # 1. Раскрываем дерево до нужных узлов
        page.expand_node("Home")

        # 2. Выбираем чекбокс и проверяем состояние
        labels_to_select = ("Home", "Documents", "Downloads")

        for label in labels_to_select:
            print(f"\n--- Чекбокс: {label} ---")
            print(f"До клика выбран: {page.is_checkbox_selected(label)}")

            page.click_checkbox(label)
            selected = page.is_checkbox_selected(label)

            print(f"После клика выбран: {selected}")
            assert selected, f"Ожидалось, что '{label}' будет выбран"

        print(f"\nРезультат на странице:\n{page.get_result_text()}")

        # 3. Снимаем выбор и проверяем снова
        page.click_checkbox("Downloads")
        assert not page.is_checkbox_selected("Downloads"), (
            "Чекбокс 'Downloads' должен быть снят после повторного клика"
        )
        print("\nЧекбокс 'Downloads' успешно снят.")

    finally:
        driver.quit()


if __name__ == "__main__":
    run_checkbox_demo()
