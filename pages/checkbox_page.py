"""
Page Object для страницы Check Box на demoqa.com.

Поддерживает два варианта разметки:
- новый: rc-tree (.rc-tree-title)
- старый: react-checkbox-tree (.rct-title)
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

OPEN_RETRIES = 3
WAIT_TIMEOUT = 30


@dataclass(frozen=True)
class _TreeLocators:
    """CSS-селекторы для конкретного типа дерева на странице."""

    node: str
    title: str
    checkbox: str
    switcher: str
    checked_class: str
    closed_class: str


# Новое дерево (rc-tree) и старое (rct) на demoqa
_RC_TREE = _TreeLocators(
    node=".rc-tree-treenode",
    title=".rc-tree-title",
    checkbox=".rc-tree-checkbox",
    switcher=".rc-tree-switcher",
    checked_class="rc-tree-checkbox-checked",
    closed_class="switcher-close",
)
_RCT_TREE = _TreeLocators(
    node=".rct-node",
    title=".rct-title",
    checkbox=".rct-checkbox",
    switcher=".rct-collapse-btn",
    checked_class="rct-checkbox-checked",
    closed_class="rct-collapse-close",
)


class CheckboxPage:
    """Страница https://demoqa.com/checkbox — работа с деревом чекбоксов."""

    URL: str = "https://demoqa.com/checkbox"
    _RESULT_BLOCK: tuple[str, str] = (By.CSS_SELECTOR, ".display-result")

    def __init__(self, driver: WebDriver, timeout: int = WAIT_TIMEOUT) -> None:
        self._driver = driver
        self._wait = WebDriverWait(driver, timeout)
        self._tree: _TreeLocators | None = None

    def open(self) -> CheckboxPage:
        """Открывает страницу с повторными попытками при обрыве соединения."""
        last_error: Exception | None = None

        for attempt in range(1, OPEN_RETRIES + 1):
            try:
                self._driver.get(self.URL)
                self._dismiss_ads()
                self._tree = self._detect_tree()
                self._wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, self._tree.title)
                    )
                )
                return self
            except WebDriverException as error:
                last_error = error
                message = str(error).lower()
                is_network = (
                    "err_connection" in message
                    or "net::" in message
                    or "timeout" in message
                    or "timed out" in message
                )
                if attempt < OPEN_RETRIES and is_network:
                    time.sleep(3 * attempt)
                    continue
                raise

        if last_error:
            raise last_error
        return self

    def _detect_tree(self) -> _TreeLocators:
        """Определяет, какое дерево отрисовалось на странице."""
        if self._driver.find_elements(By.CSS_SELECTOR, _RC_TREE.title):
            return _RC_TREE
        if self._driver.find_elements(By.CSS_SELECTOR, _RCT_TREE.title):
            return _RCT_TREE
        raise NoSuchElementException(
            "Дерево чекбоксов не найдено. Ожидались .rc-tree-title или .rct-title"
        )

    @property
    def tree(self) -> _TreeLocators:
        if self._tree is None:
            self._tree = self._detect_tree()
        return self._tree

    def _dismiss_ads(self) -> None:
        """Убирает рекламный баннер demoqa, если он перекрывает страницу."""
        self._driver.execute_script(
            """
            const ad = document.getElementById('fixedban');
            if (ad) ad.remove();
            const footer = document.getElementById('footer');
            if (footer) footer.remove();
            """
        )

    def _visible_nodes(self) -> list[WebElement]:
        """Только видимые узлы дерева (без служебных скрытых элементов)."""
        nodes = self._driver.find_elements(By.CSS_SELECTOR, self.tree.node)
        visible: list[WebElement] = []
        for node in nodes:
            if node.get_attribute("aria-hidden") == "true":
                continue
            if not node.is_displayed():
                continue
            visible.append(node)
        return visible

    def _find_node_by_title(self, title: str) -> WebElement:
        """Возвращает видимый узел дерева по тексту заголовка."""
        title = title.strip()

        for node in self._visible_nodes():
            labels = node.find_elements(By.CSS_SELECTOR, self.tree.title)
            for label in labels:
                if label.text.strip() == title:
                    self._driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});", node
                    )
                    return node

        # Запасной поиск по XPath (надёжнее при динамической подгрузке)
        xpath = (
            f"//span[contains(@class,'tree-title') or contains(@class,'rct-title')]"
            f"[normalize-space()='{title}']"
            f"/ancestor::div[contains(@class,'treenode') or contains(@class,'rct-node')][1]"
        )
        node = self._wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        self._driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", node
        )
        return node

    def expand_node(self, title: str) -> None:
        """Раскрывает дочерние элементы узла, если он свёрнут."""
        node = self._find_node_by_title(title)
        node_class = node.get_attribute("class") or ""

        switchers = node.find_elements(By.CSS_SELECTOR, self.tree.switcher)
        if switchers:
            switcher_class = switchers[0].get_attribute("class") or ""
            if self.tree.closed_class in node_class or self.tree.closed_class in switcher_class:
                switchers[0].click()
                return

        if "rct-collapse-close" in node_class:
            collapse_btn = node.find_elements(By.CSS_SELECTOR, ".rct-collapse-btn")
            if collapse_btn:
                collapse_btn[0].click()

    def click_checkbox(self, title: str) -> None:
        """Кликает по чекбоксу узла с указанным названием."""
        node = self._find_node_by_title(title)
        checkbox = node.find_element(By.CSS_SELECTOR, self.tree.checkbox)
        self._driver.execute_script("arguments[0].click();", checkbox)

    def set_checkbox(self, title: str, selected: bool) -> None:
        """Включает или выключает чекбокс до нужного состояния."""
        if self.is_checkbox_selected(title) != selected:
            self.click_checkbox(title)
            time.sleep(0.3)

    def uncheck_all(self) -> None:
        """
        Сбрасывает дерево: перезагрузка страницы — надёжно между тестами
        (после выбора Home все дочерние пункты тоже отмечены).
        """
        self._driver.refresh()
        self._dismiss_ads()
        self._tree = self._detect_tree()
        self._wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.tree.title))
        )

    def is_checkbox_selected(self, title: str) -> bool:
        """
        Проверяет, отмечен ли чекбокс полностью (aria-checked='true').

        'mixed' — частичный выбор родителя, для дочернего пункта это не «выбран».
        """
        node = self._find_node_by_title(title)
        checkbox = node.find_element(By.CSS_SELECTOR, self.tree.checkbox)

        aria_checked = checkbox.get_attribute("aria-checked")
        if aria_checked is not None:
            return aria_checked.lower() == "true"

        class_name = checkbox.get_attribute("class") or ""
        return self.tree.checked_class in class_name

    def is_label_in_result(self, label: str) -> bool:
        """Проверяет, что пункт есть в блоке 'You have selected'."""
        return label.lower() in self.get_result_text().lower()

    def get_result_text(self) -> str:
        """Возвращает текст блока 'You have selected'."""
        result = self._wait.until(EC.visibility_of_element_located(self._RESULT_BLOCK))
        return result.text.strip()
