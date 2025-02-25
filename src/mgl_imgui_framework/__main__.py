import sys
import moderngl_window
from mgl_imgui_framework import app


class DemoApp(app.App):
    title = "ModernGL ImGUI Demo"


def main():
    # Use glfw by default.
    args = sys.argv[1:]
    if "-wnd" not in args:
        args.append("-wnd")
        args.append("glfw")
    # Start the applicantion.
    moderngl_window.run_window_config(
        DemoApp,
        args=args
    )


if __name__ == "__main__":
    main()
