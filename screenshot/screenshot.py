import tkinter as tk
from PIL import ImageGrab
import time

class ScreenshotApp:
    def __init__(self, window):
        self.window = window
        window.title("")

        self.btn_capture = tk.Button(window, text="📷", font=("Comic Sans MS", 30), command=self.start_capture, bd=0, fg="blue")
        self.btn_capture.pack(padx=20, pady=(20, 2), expand=True)

        self.lbl_version = tk.Label(window, text="Release versie V1.0.1", font=("Comic Sans MS", 12), fg="grey")
        self.lbl_version.pack(pady=(0, 10))

        self.selection_overlay = None
        self.start_x = None
        self.start_y = None
        self.selection_box = None

    def start_capture(self):
        self.window.withdraw()
        time.sleep(0.5)

        self.selection_overlay = tk.Toplevel()
        self.selection_overlay.attributes("-fullscreen", True)
        self.selection_overlay.attributes("-alpha", 0.3)
        self.selection_overlay.config(bg="black")

        self.selection_overlay.bind("<ButtonPress-1>", self.begin_selection)
        self.selection_overlay.bind("<B1-Motion>", self.update_selection)
        self.selection_overlay.bind("<ButtonRelease-1>", self.finish_selection)
        self.selection_overlay.bind("<Escape>", self.cancel_capture)

        self.canvas = tk.Canvas(self.selection_overlay, cursor="pirate", bg="green")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def begin_selection(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.selection_box = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=5)

    def update_selection(self, event):
        self.canvas.coords(self.selection_box, self.start_x, self.start_y, event.x, event.y)

    def finish_selection(self, event):
        end_x, end_y = event.x, event.y

        self.selection_overlay.destroy()
        self.selection_overlay = None

        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)

        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        filename = f"screenshot_{int(time.time())}.png"
        screenshot.save(filename)

        self.window.deiconify()

    def cancel_capture(self, event=None):
        if self.selection_overlay:
            self.selection_overlay.destroy()
            self.selection_overlay = None
        self.window.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("250x150")
    root.resizable(False, False)
    app = ScreenshotApp(root)
    root.mainloop()
