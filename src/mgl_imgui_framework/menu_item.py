"""
Menu bar and status bar render target.
"""

from abc import ABC, abstractmethod


class MenuItem(ABC):
    @abstractmethod
    def render(self, time: float, frame_time: float) -> None:
        """
        Main rendering loop for menu item.

        :param time: time since the start of the application.
        :param frame_time: frame delta time.
        :raises NotImplementedError: child class is required to implement this
            method to render correctly.
        """
        raise NotImplementedError("Method not implement")
