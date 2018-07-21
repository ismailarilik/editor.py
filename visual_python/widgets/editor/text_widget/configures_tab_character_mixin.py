import tkinter as tk
import tkinter.font as tk_font
import abc
import enum

class ConfiguresTabCharacterMixin(abc.ABC):
    '''
    A mixin which provides those functionalities to implementor text widget:

    - Change tab type between tab and space
    - Change tab size
    '''
    # Declare constants
    class TabType(enum.Enum):
        TAB = enum.auto()
        SPACE = enum.auto()

    def __init__(self):
        # Initialize defaults
        self.tab_type: self.TabType = self.TabType.TAB
        self.tab_size = 8
        # Listen for Tab key press
        self.bind('<Tab>', self.on_press_tab)

    @property
    def tab_size(self):
        return self._tab_size

    @tab_size.setter
    def tab_size(self, new_tab_size: int):
        self._tab_size = new_tab_size
        # Also configure text widget tab stops with specified tab size
        font = tk_font.Font(font=self['font'])
        tab_width = font.measure(' ' * self.tab_size)
        self.config(tabs=(tab_width,))

    def on_press_tab(self, event):
        # Insert tab or space with respect to `tab_type`
        # Tab stops and spaces which will be added, are determined by `tab_size`
        if self.tab_type is self.TabType.TAB:
            tab = '\t'
        else:
            tab = ' ' * self.tab_size
        self.insert(tk.INSERT, tab)
        # Prevent additional tab character insertion by default handler
        return 'break'
