import tkinter as tk

class TextWidget(tk.Text):
    def __init__(self, master):
        super().__init__(master)

    def set_text(self, text):
        self.delete(1.0, tk.END)
        self.insert(tk.END, text)
