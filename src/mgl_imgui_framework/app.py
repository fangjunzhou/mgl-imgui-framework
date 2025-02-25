"""
Main application.
"""

import logging
from typing import Any, Optional
import moderngl
import argparse
from imgui_bundle import imgui
from moderngl_window.integrations.imgui_bundle import ModernglWindowRenderer
from moderngl_window.context.base import BaseWindow, KeyModifiers, WindowConfig
from moderngl_window.timers import BaseTimer


logger = logging.getLogger(__name__)


class App(WindowConfig):
    # ---------------------- Window Config  ---------------------- #

    title = "ModernGL ImGUI Default Window"
    gl_version = (3, 3)
    window_size = (960, 540)
    resizable = True
    aspect_ratio = None

    # ------------------------ App State  ------------------------ #

    io: imgui.IO
    imgui_renderer: ModernglWindowRenderer

    window_time: float = 0

    def __init__(self,
                 ctx: Optional[moderngl.Context] = None,
                 wnd: Optional[BaseWindow] = None,
                 timer: Optional[BaseTimer] = None,
                 **kwargs: Any) -> None:
        super().__init__(ctx, wnd, timer, **kwargs)
        # Initialize logging.
        if self.argv:
            log_level_arg: str = self.argv.log
            if log_level_arg == "INFO":
                self.log_level = logging.INFO
            elif log_level_arg == "WARN":
                self.log_level = logging.WARN
            elif log_level_arg == "DEBUG":
                self.log_level = logging.DEBUG
            elif log_level_arg == "ERROR":
                self.log_level = logging.ERROR
            else:
                raise ValueError(f"Log level {log_level_arg} doesn't exist.")
        logging.basicConfig(
            level=self.log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        logger.info("WindowConfig initialized.")
        logger.info(f"Current OpenGL version: {self.gl_version}")
        # Disable exit key.
        self.wnd.exit_key = None
        # Initialize ModernGL context.
        self.ctx.gc_mode = "auto"
        logger.info(f"Using gc_mode: {self.ctx.gc_mode}")
        # Initialize ImGui
        imgui.create_context()
        self.io = imgui.get_io()
        self.io.set_ini_filename("")
        self.io.set_log_filename("")
        # Initialize renderer.
        self.imgui_renderer = ModernglWindowRenderer(self.wnd)

    @classmethod
    def add_arguments(cls, parser: argparse.ArgumentParser):
        parser.add_argument(
            "-l",
            "--log",
            choices=["INFO", "WARN", "DEBUG", "ERROR"],
            default="WARN",
            type=str
        )

    def on_resize(self, width: int, height: int) -> None:
        self.imgui_renderer.resize(width, height)
        self.wnd.render(self.timer.time, self.timer.time - self.window_time)
        self.wnd.swap_buffers()

    def on_close(self) -> None:
        pass

    def on_iconify(self, iconified: bool) -> None:
        pass

    def on_key_event(
            self,
            key: Any,
            action: Any,
            modifiers: KeyModifiers) -> None:
        self.imgui_renderer.key_event(key, action, modifiers)

    def on_unicode_char_entered(self, char: str) -> None:
        self.imgui_renderer.unicode_char_entered(char)

    def on_mouse_position_event(self, x: int, y: int, dx: int, dy: int) -> None:
        self.imgui_renderer.mouse_position_event(x, y, dx, dy)

    def on_mouse_drag_event(self, x: int, y: int, dx: int, dy: int) -> None:
        self.imgui_renderer.mouse_drag_event(x, y, dx, dy)

    def on_mouse_scroll_event(self, x_offset: float, y_offset: float) -> None:
        self.imgui_renderer.mouse_scroll_event(x_offset, y_offset)

    def on_mouse_press_event(self, x: int, y: int, button: int) -> None:
        self.imgui_renderer.mouse_press_event(x, y, button)

    def on_mouse_release_event(self, x: int, y: int, button: int) -> None:
        self.imgui_renderer.mouse_release_event(x, y, button)

    def on_render(self, time: float, frame_time: float) -> None:
        self.window_time = time
