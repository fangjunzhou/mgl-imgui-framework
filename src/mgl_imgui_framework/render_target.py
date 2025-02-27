"""
A render target that can be handled by ImGUI.
"""

from abc import ABC, abstractmethod


class RenderTarget(ABC):
    @abstractmethod
    def render(self, time: float, frame_time: float) -> None:
        """
        Main rendering loop for the window.

        :param time: time since the start of the application.
        :param frame_time: frame delta time.
        :raises NotImplementedError: child class is required to implement this
            method to render correctly.
        """
        raise NotImplementedError("Method not implement")
