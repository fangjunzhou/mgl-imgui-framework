"""
The entry point for example application.
"""

import sys
import moderngl_window

from mgl_imgui_framework.examples.app import DemoApp


def main():
    # Use glfw by default.
    args = sys.argv[1:]
    if "-wnd" not in args:
        args.append("-wnd")
        args.append("glfw")
    # Start the applicantion.
    moderngl_window.run_window_config(DemoApp, args=args)


if __name__ == "__main__":
    main()
