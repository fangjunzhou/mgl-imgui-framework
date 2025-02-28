"""
A example application.
"""

from typing import Any, Optional
import moderngl
from moderngl_window.context.base import BaseWindow
from moderngl_window.timers import BaseTimer
from reactivex.subject import BehaviorSubject
from mgl_imgui_framework.app import App
from mgl_imgui_framework.examples.counter.counter import CounterWindow
from mgl_imgui_framework.examples.demo.imgui_demo import ImGUIDemoWindow
from mgl_imgui_framework.examples.dockspace_builder import DemoBuilder
from mgl_imgui_framework.examples.multiprocessing.mp_window import MPWindow
from mgl_imgui_framework.render_targets.menu_item import MenuItem
from mgl_imgui_framework.utils.fps_counter import FpsCounter
from mgl_imgui_framework.hierachical_menu_item import HierarchicalMenuItem


class DemoApp(App):
    # Window config.
    title = "ModernGL ImGUI Demo"

    # Window state.
    demo_window_opened: BehaviorSubject[bool] = BehaviorSubject(True)
    counter_window_opened: BehaviorSubject[bool] = BehaviorSubject(True)
    mp_window_opened: BehaviorSubject[bool] = BehaviorSubject(True)

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
        imgui_demo_menu_item = MenuItem(
            "ImGUI Demo Window",
            self.demo_window_opened,
            set_demo_window_opened)

        # ---------------------- Counter Window ---------------------- #

        def set_counter_window_opened(new_opened: bool):
            self.counter_window_opened.on_next(new_opened)
        counter_window = CounterWindow(
            self.counter_window_opened,
            lambda: set_counter_window_opened(False))
        counter_menu_item = MenuItem(
            "Counter Window",
            self.counter_window_opened,
            set_counter_window_opened)

        # ------------------ Multiprocessing Window ------------------ #
        def set_mp_window_opened(new_opened: bool):
            self.mp_window_opened.on_next(new_opened)
        mp_window = MPWindow(
            self.mp_window_opened,
            lambda: set_mp_window_opened(False))
        mp_menu_item = MenuItem(
            "Multiprocessing Window",
            self.mp_window_opened,
            set_mp_window_opened)

        # -------------------- Example Menu Item  -------------------- #
        example_menu_item = HierarchicalMenuItem("Example")
        example_menu_item.menu_items.append(imgui_demo_menu_item)
        example_menu_item.menu_items.append(counter_menu_item)
        example_menu_item.menu_items.append(mp_menu_item)

        # Register windows.
        self.render_targets.append(imgui_demo_window)
        self.render_targets.append(counter_window)
        self.render_targets.append(mp_window)
        # Register menu item.
        self.dockspace.menu_items.append(example_menu_item)
        # Register status bar item.
        self.dockspace.status_items.append(FpsCounter())

        # Load dockspace builder.
        self.dockspace.builder = DemoBuilder()
