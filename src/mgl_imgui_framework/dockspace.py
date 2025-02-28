"""
Dockspace render target.
Includes main menu bar, dockspace, and status bar.
"""

from typing import List
from imgui_bundle import imgui, imgui_ctx
from reactivex import Observable

from mgl_imgui_framework.render_target import RenderTarget


class DockspaceBuilder:
    def build(self, dockspace_id: int):
        pass


class Dockspace(RenderTarget):
    wnd_size: tuple[int, int] = (0, 0)
    builder: DockspaceBuilder | None

    # --------------------- Dockspace State  --------------------- #

    menu_items: List[RenderTarget] = []
    status_items: List[RenderTarget] = []

    def __init__(self,
                 wnd_size: Observable[tuple[int,
                                            int]],
                 builder: DockspaceBuilder | None = None) -> None:
        def set_size(size: tuple[int, int]):
            self.wnd_size = size
        wnd_size.subscribe(set_size)
        self.builder = builder

    def render(self, time: float, frame_time: float) -> None:
        # Menu bar.
        with imgui_ctx.begin_main_menu_bar():
            for status_item in self.menu_items:
                status_item.render(time, frame_time)

        # Dockspace.
        side_bar_height = imgui.get_frame_height()
        imgui.set_next_window_pos((0, side_bar_height))
        imgui.set_next_window_size(
            (self.wnd_size[0], self.wnd_size[1] - 2 * side_bar_height))
        window_flags = (imgui.WindowFlags_.no_title_bar.value |
                        imgui.WindowFlags_.no_collapse.value |
                        imgui.WindowFlags_.no_resize.value |
                        imgui.WindowFlags_.no_move.value |
                        imgui.WindowFlags_.no_bring_to_front_on_focus.value |
                        imgui.WindowFlags_.no_nav_focus.value |
                        imgui.WindowFlags_.no_background.value)
        with imgui_ctx.begin("Dockspace Window", True, window_flags):
            # Dockspace.
            dockspace_id = imgui.get_id("Dockspace")
            if self.builder:
                self.builder.build(dockspace_id)
            imgui.dock_space(dockspace_id)

        # Status bar.
        imgui.set_next_window_pos(
            (0, self.wnd_size[1] - side_bar_height))
        imgui.set_next_window_size(
            (self.wnd_size[0], side_bar_height))
        window_flags = (imgui.WindowFlags_.no_title_bar.value |
                        imgui.WindowFlags_.no_collapse.value |
                        imgui.WindowFlags_.menu_bar.value |
                        imgui.WindowFlags_.no_resize.value |
                        imgui.WindowFlags_.no_move.value |
                        imgui.WindowFlags_.no_bring_to_front_on_focus.value |
                        imgui.WindowFlags_.no_nav_focus.value |
                        imgui.WindowFlags_.no_background.value)
        with imgui_ctx.begin("Status Bar", True, window_flags):
            with imgui_ctx.begin_menu_bar():
                for status_item in self.status_items:
                    status_item.render(time, frame_time)
