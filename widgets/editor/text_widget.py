import tkinter as tk

class TextWidget(tk.Text):
    def __init__(self, master):
        super().__init__(master, wrap=tk.NONE)

    def get_wo_eol(self):
        '''
        Get without (automatically added) final end-of-line character
        '''
        return self.get(1.0, tk.END)[:-1]

    def set_text(self, text):
        self.delete(1.0, tk.END)
        self.insert(tk.END, text)
