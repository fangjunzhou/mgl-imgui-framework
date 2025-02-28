"""
A classic counter demo.
"""

from collections.abc import Callable
from imgui_bundle import imgui, imgui_ctx
from reactivex import Observable
from reactivex.subject import BehaviorSubject
from mgl_imgui_framework.render_target import RenderTarget
from mgl_imgui_framework.window import Window


class CounterMenuItem(RenderTarget):
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
        changed, new_open = imgui.menu_item("Counter Window", "", self.open)
        if changed:
            self.on_change(new_open)


class CounterWindow(Window):
    count: BehaviorSubject[int] = BehaviorSubject(0)

    def __init__(
        self,
        open: Observable[bool] | None = None,
        on_close: Callable[[],
                           None] | None = None) -> None:
        super().__init__("Counter", open, on_close)

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
