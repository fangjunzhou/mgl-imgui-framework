"""
A example application.
"""

from typing import Any, Optional
import moderngl
from moderngl_window.context.base import BaseWindow
from moderngl_window.timers import BaseTimer
from reactivex.subject import BehaviorSubject
from mgl_imgui_framework.app import App
from mgl_imgui_framework.examples.imgui_demo import ImGUIDemoMenuItem, ImGUIDemoWindow


class DemoApp(App):
    # Window config.
    title = "ModernGL ImGUI Demo"

    # Window state.
    demo_window_opened: BehaviorSubject[bool] = BehaviorSubject(False)

    def __init__(self,
                 ctx: Optional[moderngl.Context] = None,
                 wnd: Optional[BaseWindow] = None,
                 timer: Optional[BaseTimer] = None,
                 **kwargs: Any) -> None:
        super().__init__(ctx, wnd, timer, **kwargs)

        def set_demo_window_opened(new_opened: bool):
            self.demo_window_opened.on_next(new_opened)
        # Register windows.
        self.windows.append(
            ImGUIDemoWindow(
                self.demo_window_opened,
                lambda: set_demo_window_opened(False)))
        # Register menu item.
        self.dockspace.menu_items.append(
            ImGUIDemoMenuItem(
                self.demo_window_opened,
                set_demo_window_opened))
