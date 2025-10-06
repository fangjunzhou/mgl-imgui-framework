from imgui_bundle import imgui
from mgl_imgui_framework.dockspace import DockspaceBuilder


class DemoBuilder(DockspaceBuilder):
    def build(self, dockspace_id: int):
        # Build dock space.
        if not imgui.internal.dock_builder_get_node(dockspace_id):
            imgui.internal.dock_builder_remove_node(dockspace_id)
            imgui.internal.dock_builder_add_node(dockspace_id)
            res = imgui.internal.dock_builder_split_node(
                dockspace_id, imgui.Dir.left, 0.7
            )
            demo_window = res.id_at_dir
            sub_windows = res.id_at_opposite_dir
            res = imgui.internal.dock_builder_split_node(sub_windows, imgui.Dir.up, 0.5)
            counter_window = res.id_at_dir
            mp_window = res.id_at_opposite_dir
            imgui.internal.dock_builder_dock_window("Dear ImGui Demo", demo_window)
            imgui.internal.dock_builder_dock_window("Counter Window", counter_window)
            imgui.internal.dock_builder_dock_window("Multiprocessing Window", mp_window)
            imgui.internal.dock_builder_finish(dockspace_id)
