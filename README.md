# DemoQA Checkbox — автоматизация на Selenium

Автотесты для страницы [Check Box](https://demoqa.com/checkbox) на demoqa.com: выбор чекбоксов в дереве и проверка их состояния.

## Возможности

- Page Object (`pages/checkbox_page.py`)
- Поддержка разметки **rc-tree** и **rct** (старая версия demoqa)
- Проверка состояния по `aria-checked` и CSS-классам
- Автотесты на **pytest**
- Демо-скрипт для ручного запуска

## Требования

- Python 3.11+ (рекомендуется 3.12; на 3.14 тоже работает)
- Google Chrome

## Установка

```bash
git clone https://github.com/<ваш-логин>/demoqa-checkbox.git
cd demoqa-checkbox
python -m venv venv
```

**Windows (CMD):**

```cmd
venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Запуск

Демо-скрипт:

```bash
python main.py
```

Все тесты:

```bash
python -m pytest -v
```

Или двойной клик по `run_tests.bat` (Windows).

## Структура проекта

```
demoqa-checkbox/
├── pages/
│   └── checkbox_page.py   # Page Object
├── tests/
│   └── test_checkbox.py   # Автотесты
├── driver_setup.py        # Настройка Chrome
├── main.py                # Демо-скрипт
├── requirements.txt
├── pytest.ini
├── run_demo.bat
└── run_tests.bat
```

## Тесты

| Тест | Описание |
|------|----------|
| `test_select_home_checkbox` | Выбор чекбокса Home |
| `test_expand_and_select_documents` | Раскрытие дерева и выбор Documents |
| `test_toggle_checkbox_state` | Повторный клик снимает выбор |

## Примечания

- Сайт demoqa.com должен открываться в обычном браузере.
- Если установлен глобальный `pytest-selenium`, он может конфликтовать с Python 3.12+ — в `pytest.ini` плагин отключён.
- Между тестами страница перезагружается (`uncheck_all`), чтобы тесты не влияли друг на друга.

## Лицензия

MIT
