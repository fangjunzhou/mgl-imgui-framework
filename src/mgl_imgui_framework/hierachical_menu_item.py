"""
Expandable hierarchical menu item.
"""

from typing import List

from imgui_bundle import imgui
from mgl_imgui_framework.render_target import RenderTarget


class HierarchicalMenuItem(RenderTarget):
    name: str
    menu_items: List[RenderTarget]

    def __init__(self, name: str) -> None:
        self.name = name
        self.menu_items = []

    def render(self, time: float, frame_time: float) -> None:
        if imgui.begin_menu(self.name):
            for menu_item in self.menu_items:
                menu_item.render(time, frame_time)
            imgui.end_menu()
