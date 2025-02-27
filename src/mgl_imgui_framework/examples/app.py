"""
A example application.
"""

from typing import Any, Optional
import moderngl
from moderngl_window.context.base import BaseWindow
from moderngl_window.timers import BaseTimer
from reactivex.subject import BehaviorSubject
from mgl_imgui_framework.app import App
from mgl_imgui_framework.examples.counter.counter import CounterMenuItem, CounterWindow
from mgl_imgui_framework.examples.demo.imgui_demo import ImGUIDemoMenuItem, ImGUIDemoWindow
from mgl_imgui_framework.utils.fps_counter import FpsCounter
from mgl_imgui_framework.utils.hierachical_menu_item import HierarchicalMenuItem


class DemoApp(App):
    # Window config.
    title = "ModernGL ImGUI Demo"

    # Window state.
    demo_window_opened: BehaviorSubject[bool] = BehaviorSubject(False)
    counter_window_opened: BehaviorSubject[bool] = BehaviorSubject(False)

    def __init__(self,
                 ctx: Optional[moderngl.Context] = None,
                 wnd: Optional[BaseWindow] = None,
                 timer: Optional[BaseTimer] = None,
                 **kwargs: Any) -> None:
        super().__init__(ctx, wnd, timer, **kwargs)

        # -------------------- ImGUI Demo Window  -------------------- #

        def set_demo_window_opened(new_opened: bool):
            self.demo_window_opened.on_next(new_opened)
        imgui_demo_window = ImGUIDemoWindow(
            self.demo_window_opened,
            lambda: set_demo_window_opened(False))
        imgui_demo_menu_item = ImGUIDemoMenuItem(
            self.demo_window_opened, set_demo_window_opened)

        # ---------------------- Counter Window ---------------------- #

        def set_counter_window_opened(new_opened: bool):
            self.counter_window_opened.on_next(new_opened)
        counter_window = CounterWindow(
            self.counter_window_opened,
            lambda: set_counter_window_opened(False))
        counter_menu_item = CounterMenuItem(
            self.counter_window_opened, set_counter_window_opened)

        # -------------------- Example Menu Item  -------------------- #
        example_menu_item = HierarchicalMenuItem("Example")
        example_menu_item.menu_items.append(imgui_demo_menu_item)
        example_menu_item.menu_items.append(counter_menu_item)

        # Register windows.
        self.windows.append(imgui_demo_window)
        self.windows.append(counter_window)
        # Register menu item.
        self.dockspace.menu_items.append(example_menu_item)
        # Register status bar item.
        self.dockspace.status_items.append(FpsCounter())
