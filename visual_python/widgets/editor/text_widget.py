import tkinter as tk
from .listens_modified_event_mixin import ListensModifiedEventMixin
from .colorizable_mixin import ColorizableMixin

class TextWidget(tk.Text, ListensModifiedEventMixin, ColorizableMixin):
    def __init__(self, master, app):
        super().__init__(master, undo=True, wrap=tk.NONE)
        ListensModifiedEventMixin.__init__(self)
        ColorizableMixin.__init__(self)
        self.app = app
        # Handle open file event here, too for this widget and prevent propagation of event
        # Because default behavior of this widget is not wanted here
        self.bind('<Control-KeyPress-o>', self._handle_open_file_event_and_prevent_propagation)
        # Set vertical and horizontal scrollbars
        vertical_scrollbar = tk.Scrollbar(self.master)
        vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        vertical_scrollbar.config(command=self.yview)
        horizontal_scrollbar = tk.Scrollbar(self.master, orient=tk.HORIZONTAL)
        horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        horizontal_scrollbar.config(command=self.xview)
        self.config(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)

    def _handle_open_file_event_and_prevent_propagation(self, event):
        self.app.handle_open_file_event(event)
        return 'break'

    def get_wo_eol(self):
        '''
        Get without (automatically added) final end-of-line character
        '''
        return self.get(1.0, tk.END)[:-1]

    def set_text(self, text):
        self.delete(1.0, tk.END)
        self.insert(tk.END, text)

    def modified(self, event):
        self.colorize()
        # Prefix current title with asterisk if it is not exist
        title = self.app.title()
        title = title if title.startswith('*') else f'*{title}'
        self.app.title(title)
