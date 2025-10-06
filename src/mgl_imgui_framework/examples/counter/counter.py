"""
A classic counter demo.
"""

from collections.abc import Callable
from imgui_bundle import imgui
from reactivex import Observable
from reactivex.subject import BehaviorSubject
from mgl_imgui_framework.render_targets.window import Window


class CounterWindow(Window):
    count: BehaviorSubject[int] = BehaviorSubject(0)

    def __init__(
        self,
        open: Observable[bool] | None = None,
        on_close: Callable[[], None] | None = None,
    ) -> None:
        super().__init__("Counter Window", open, on_close)

    def increase(self):
        self.count.on_next(self.count.value + 1)

    def clear(self):
        self.count.on_next(0)

    def render_window(self, time: float, frame_time: float) -> None:
        imgui.text(f"Current count: {self.count.value}")

        if imgui.button("Increase"):
            self.increase()
        if imgui.button("Clear"):
            self.clear()
