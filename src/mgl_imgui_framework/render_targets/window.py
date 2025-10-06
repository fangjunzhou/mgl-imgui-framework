"""
Window base class that handles basic window interaction.
"""

from collections.abc import Callable
from imgui_bundle import imgui, imgui_ctx
from reactivex import Observable
from mgl_imgui_framework.render_target import RenderTarget


class Window(RenderTarget):
    # Window name.
    name: str
    size: tuple[int, int] = (480, 320)
    size_min: tuple[int, int] = (0, 0)
    size_max: tuple[int, int] = (0, 0)
    window_flags: int = imgui.WindowFlags_.none.value

    # Window open state.
    open: bool | None
    # Close window callback.
    on_close: Callable[[], None] | None

    def __init__(
        self,
        name: str,
        open: Observable[bool] | None = None,
        on_close: Callable[[], None] | None = None,
    ) -> None:
        self.name = name
        # Subscribe open window state.

        def set_open(open: bool):
            self.open = open
            self.on_open_changed(open)

        if open is not None:
            open.subscribe(set_open)
        else:
            self.open = None

        # Set close window callback.
        self.on_close = on_close

    def on_open_changed(self, open: bool):
        """This method is called when self.open state changed.

        :param open: new open state.
        """
        pass

    def render(self, time: float, frame_time: float) -> None:
        if self.open is None or self.open:
            imgui.set_next_window_size(self.size, imgui.Cond_.once.value)
            imgui.set_next_window_size_constraints(self.size_min, self.size_max)
            with imgui_ctx.begin(self.name, self.open, self.window_flags) as window:
                if not window.opened and self.on_close is not None:
                    self.on_close()
                self.render_window(time, frame_time)

    def render_window(self, time: float, frame_time: float) -> None:
        """
        Main rendering loop for Window.

        :param time: time since the start of the application.
        :param frame_time: frame delta time.
        :raises NotImplementedError: child class is required to implement this
            method to render correctly.
        """
        raise NotImplementedError("Method not implement")
