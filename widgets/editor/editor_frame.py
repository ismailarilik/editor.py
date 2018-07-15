import tkinter as tk
from .text_widget import TextWidget

class EditorFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # Add text widget
        self.text_widget = TextWidget(self)
        self.text_widget.pack(fill=tk.BOTH, expand=True)

    def set_text(self, text):
        self.text_widget.set_text(text)
