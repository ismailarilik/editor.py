import tkinter as tk
from .text_widget import TextWidget

class EditorFrame(tk.Frame):
    def __init__(self, master, prefix_current_title, remove_title_prefix):
        super().__init__(master)
        self.prefix_current_title = prefix_current_title
        self.remove_title_prefix = remove_title_prefix
        # Add text widget
        self.text_widget = TextWidget(self, self.modified)
        self.text_widget.pack(fill=tk.BOTH, expand=True)

    def get_text(self):
        return self.text_widget.get_wo_eol()

    def set_text(self, text):
        self.text_widget.set_text(text)

    def modified(self, event, programmatically):
        # Prefix current title with asterisk if modified manually
        # Remove it otherwise
        if not programmatically:
            self.prefix_current_title('*', '')
        else:
            self.remove_title_prefix('*')
