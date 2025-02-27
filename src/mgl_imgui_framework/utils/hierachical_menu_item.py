from typing import List

from imgui_bundle import imgui
from mgl_imgui_framework.menu_item import MenuItem


class HierarchicalMenuItem(MenuItem):
    name: str
    menu_items: List[MenuItem]

    def __init__(self, name: str) -> None:
        self.name = name
        self.menu_items = []

    def render(self, time: float, frame_time: float) -> None:
        if imgui.begin_menu(self.name):
            for menu_item in self.menu_items:
                menu_item.render(time, frame_time)
            imgui.end_menu()
