"""
The mgl_imgui wrapper for imgui demo window.
"""

from collections.abc import Callable
from imgui_bundle import imgui
from reactivex import Observable
from mgl_imgui_framework.render_targets.window import Window


class ImGUIDemoWindow(Window):
    def __init__(
        self,
        open: Observable[bool] | None = None,
        on_close: Callable[[], None] | None = None,
    ) -> None:
        super().__init__("ImGUI Demo Window", open, on_close)

    def render(self, time: float, frame_time: float) -> None:
        if self.open is None or self.open:
            if not imgui.show_demo_window(self.open):
                if self.on_close is not None:
                    self.on_close()
