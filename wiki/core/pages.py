from collections.abc import Callable
from typing import List

from flask import Flask

from wiki.core.models.pages import Page


class PagesManager:
    _core_renderers: List[Callable[[Page, str], str]] = []
    _user_renderers: List[Callable[[Page, str], str]] = []
    _menu_actions = []
    _views = []

    def __init__(self):
        pass

    def init_app(self, app: Flask):
        pass

    def add_view(self, name: str, label: str, url: str, order: int = 0):
        self._views.append(
            {
                "name": name,
                "label": label,
                "url": url,
                "order": order or len(self._views),
            }
        )

    def add_menu_action(
        self, name: str, label: str, url: str, icon: str, order: int = 0
    ):
        self._menu_actions.append(
            {
                "name": name,
                "label": label,
                "url": url,
                "icon": icon,
                "order": order or len(self._menu_actions),
            }
        )

    def add_renderer(self, renderer: Callable[[Page, str], str]):
        self._user_renderers.append(renderer)

    def render(self, page: Page, content: str) -> str:
        # Do user renderers first
        current_state = content
        for r in self._user_renderers:
            current_state = r(page, current_state)

        # Then do the core/system renderers
        for r in self._core_renderers:
            current_state = r(page, current_state)

        return current_state


pages_manager = PagesManager()
