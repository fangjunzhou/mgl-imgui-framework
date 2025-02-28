"""
The mgl_imgui wrapper for imgui demo window.
"""

from collections.abc import Callable
from imgui_bundle import imgui
from reactivex import Observable
from mgl_imgui_framework.render_target import RenderTarget
from mgl_imgui_framework.window import Window


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


class ImGUIDemoWindow(Window):
    def __init__(
        self,
        open: Observable[bool] | None = None,
        on_close: Callable[[],
                           None] | None = None) -> None:
        super().__init__("ImGUI Demo Window", open, on_close)

    def render(self, time: float, frame_time: float) -> None:
        if self.open is None or self.open:
            if not imgui.show_demo_window(self.open):
                if self.on_close is not None:
                    self.on_close()
