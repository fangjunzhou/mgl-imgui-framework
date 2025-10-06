"""
A multiprocessing demo.
"""

from collections.abc import Callable
import logging
import multiprocessing as mp
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
import time

from imgui_bundle import imgui
from reactivex import Observable

from mgl_imgui_framework.render_targets.window import Window


logger = logging.getLogger(__name__)


def worker_main(conn: Connection):
    """Worker entry point.

    :param conn: child connection passed to worker process.
    """
    idx = 1
    while True:
        # Terminate worker.
        if conn.poll() and conn.recv():
            break
        conn.send(idx)
        time.sleep(1)
        idx += 1


class MPWindow(Window):
    # Worker process.
    worker: Process | None = None
    # Parent connection.
    conn: Connection | None = None
    # Worker message.
    worker_msg: int | None = None

    def __init__(
        self,
        open: Observable[bool] | None = None,
        on_close: Callable[[], None] | None = None,
    ) -> None:
        super().__init__("Multiprocessing Window", open, on_close)

    def start_worker(self):
        if self.worker:
            logger.warning("There's already a worker running.")
            return
        parent_conn, child_conn = Pipe()
        self.conn = parent_conn
        self.worker = Process(target=worker_main, args=(child_conn,))
        self.worker.start()
        logger.info("Worker started.")

    def terminate_worker(self):
        if not self.conn or not self.worker:
            logger.warning("No running worker.")
            return
        self.conn.send(True)
        self.worker = None
        self.conn = None
        self.worker_msg = None
        logger.info("Worker terminated.")

    def on_exit(self):
        if self.worker:
            self.terminate_worker()
            # Hard terminate worker:
            # self.worker.kill()

    def render_window(self, time: float, frame_time: float) -> None:
        # Receive worker message.
        if self.conn and self.conn.poll():
            self.worker_msg = self.conn.recv()
            logger.info("Received worker message.")
        # Display worker message.
        if self.worker_msg:
            imgui.text(f"Worker message: {self.worker_msg}")
        else:
            imgui.text("No worker message")

        # Start and terminate worker.
        if imgui.button("Start Worker"):
            self.start_worker()
        if imgui.button("Terminate Worker"):
            self.terminate_worker()
