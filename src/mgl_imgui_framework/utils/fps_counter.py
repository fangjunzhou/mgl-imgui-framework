from typing import List
from imgui_bundle import imgui
from mgl_imgui_framework.render_target import RenderTarget


class FpsCounter(RenderTarget):
    buf: List[float]
    idx: int = 0
    disp_fps: int = 0

    def __init__(self, buf_size: int = 15) -> None:
        self.buf = [0 for _ in range(buf_size)]

    def render(self, time: float, frame_time: float) -> None:
        self.buf[self.idx] = frame_time
        self.idx = (self.idx + 1) % len(self.buf)
        if self.idx == 0:
            avg_frame_time = sum(self.buf) / len(self.buf)
            self.disp_fps = int(1 / avg_frame_time)
        imgui.text(f"{self.disp_fps} FPS")
