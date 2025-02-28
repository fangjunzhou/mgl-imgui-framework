"""
MenuItem class that handles its open state.
"""


from collections.abc import Callable

from imgui_bundle import imgui
from reactivex import Observable
from mgl_imgui_framework.render_target import RenderTarget


class MenuItem(RenderTarget):
    # MenuItem name.
    name: str
    # MenuItem open state.
    open: bool
    # Change open status callback.
    on_change: Callable[[bool], None] | None

    def __init__(
            self,
            name: str,
            open: Observable[bool],
            on_change: Callable[[bool], None] | None) -> None:
        self.name = name

        def set_open(open: bool):
            self.open = open
        open.subscribe(set_open)
        self.on_change = on_change

    def render(self, time: float, frame_time: float) -> None:
        # TODO: Handle shortcut.
        changed, new_open = imgui.menu_item(self.name, "", self.open)
        if changed and self.on_change:
            self.on_change(new_open)
