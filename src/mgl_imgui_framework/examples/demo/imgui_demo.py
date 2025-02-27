"""
The mgl_imgui wrapper for imgui demo window.
"""

from collections.abc import Callable
from imgui_bundle import imgui
from reactivex import Observable
from mgl_imgui_framework.render_target import RenderTarget


class ImGUIDemoMenuItem(RenderTarget):
    # Window open state.
    open: bool
    # Change open status callback.
    on_change: Callable[[bool], None]

    def __init__(
        self,
        open: Observable[bool],
        on_change: Callable[[bool],
                            None]) -> None:
        def set_open(open: bool):
            self.open = open
        open.subscribe(set_open)
        self.on_change = on_change

    def render(self, time: float, frame_time: float) -> None:
        changed, new_open = imgui.menu_item("ImGUI Demo Window", "", self.open)
        if changed:
            self.on_change(new_open)


class ImGUIDemoWindow(RenderTarget):
    # Window open state.
    open: bool
    # Close window callback.
    on_close: Callable[[], None]

    def __init__(
        self,
        open: Observable[bool],
        on_close: Callable[[],
                           None]) -> None:
        def set_open(open: bool):
            self.open = open
        open.subscribe(set_open)
        self.on_close = on_close

    def render(self, time: float, frame_time: float) -> None:
        if self.open:
            if not imgui.show_demo_window(self.open):
                self.on_close()
