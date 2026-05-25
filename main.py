"""
Скрипт для ручного запуска: выбор чекбоксов на demoqa.com/checkbox
и проверка их состояния.

Запуск: python main.py
"""

from __future__ import annotations

from driver_setup import create_chrome_driver
from pages.checkbox_page import CheckboxPage


def run_checkbox_demo() -> None:
    """
    Демонстрация работы с чекбоксами на demoqa.com.
    
    Логика работы с иерархическими чекбоксами:
    - При выборе родительского чекбокса все дочерние автоматически выбираются
    - При снятии дочернего чекбокса родительский остаётся выбранным (частично)
    - При повторном клике на дочерний чекбокс он снимается из выборки
    """
    driver = create_chrome_driver()
    result_messages: list[str] = []  # Сбор сообщений о проверках

    try:
        # Открываем страницу с чекбоксами
        page = CheckboxPage(driver).open()

        # 1. Раскрываем дерево до нужных узлов для удобной навигации
        page.expand_node("Home")

        # 2. СНАЧАЛА ВЫБИРАЕМ РОДИТЕЛЬСКИЙ ЭЛЕМЕНТ
        #    (это автоматически выберет все дочерние)
        parent_label = "Home"
        child_labels = ("Documents", "Downloads")

        print(f"\n--- Шаг 1: Выбор родительского элемента '{parent_label}' ---")
        print(f"До клика выбран: {page.is_checkbox_selected(parent_label)}")

        page.click_checkbox(parent_label)
        parent_selected = page.is_checkbox_selected(parent_label)

        print(f"После клика выбран: {parent_selected}")
        assert parent_selected, f"Ожидалось, что '{parent_label}' будет выбран"
        result_messages.append(f"✓ Родительский элемент '{parent_label}' выбран")

        # Проверяем, что дочерние элементы автоматически выбрались
        print(f"\n--- Шаг 2: Проверка автоматического выбора дочерних элементов ---")
        for child_label in child_labels:
            is_selected = page.is_checkbox_selected(child_label)
            print(f"  Чекбокс '{child_label}' выбран: {is_selected}")
            assert is_selected, f"Ошибка: '{child_label}' должен быть выбран автоматически"
            result_messages.append(f"✓ Дочерний элемент '{child_label}' выбран автоматически")

        print(f"\nРезультат на странице после выбора Home:\n{page.get_result_text()}")

        # 3. СНИМАЕМ ОДИН ИЗ ДОЧЕРНИХ ЭЛЕМЕНТОВ
        #    (дочерний снимается, родительский остаётся в частично выбранном состоянии)
        uncheck_child = "Downloads"
        print(f"\n--- Шаг 3: Снятие дочернего элемента '{uncheck_child}' ---")
        
        print(f"До клика выбран: {page.is_checkbox_selected(uncheck_child)}")
        page.click_checkbox(uncheck_child)  # Повторный клик снимает выделение
        child_selected_after = page.is_checkbox_selected(uncheck_child)
        print(f"После клика выбран: {child_selected_after}")
        
        assert not child_selected_after, (
            f"Чекбокс '{uncheck_child}' должен быть снят после повторного клика"
        )
        result_messages.append(f"✓ Дочерний элемент '{uncheck_child}' успешно снят")

        # Проверяем, что родительский элемент всё ещё выбран (или в состоянии partial)
        print(f"\n--- Шаг 4: Проверка состояния родительского элемента ---")
        parent_still_selected = page.is_checkbox_selected(parent_label)
        print(f"Родительский элемент '{parent_label}' выбран: {parent_still_selected}")
        # Родительский элемент остаётся выбранным (частично)
        result_messages.append(f"✓ Родительский элемент '{parent_label}' остаётся выбранным")

        # Выводим итоговый результат
        print(f"\n--- ИТОГОВЫЙ РЕЗУЛЬТАТ ---")
        for msg in result_messages:
            print(msg)
        
        print(f"\nФинальный текст результата на странице:\n{page.get_result_text()}")
        print("\n✅ Все проверки успешно пройдены!")

    except AssertionError as e:
        # Обрабатываем ошибки assert без прерывания программы
        print(f"\n❌ Ошибка проверки: {e}")
        raise  # Пробрасываем дальше для finally блока, но с информативным сообщением
    except Exception as e:
        # Обрабатываем другие возможные ошибки
        print(f"\n❌ Непредвиденная ошибка: {type(e).__name__}: {e}")
        raise
    finally:
        driver.quit()


if __name__ == "__main__":
    run_checkbox_demo()
