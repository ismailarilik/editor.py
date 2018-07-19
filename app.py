import tkinter as tk
from widgets.main_frame import MainFrame
from menus.main_menu import MainMenu

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Set app title
        self.app_title = 'Visual Python'
        self.title(self.app_title)
        # Prefix app title with unsaved file specifier
        self.prefix_app_title('(Unsaved File)')
        # Set app icon
        self.iconbitmap('icon.ico')
        # Add main frame
        self.main_frame = MainFrame(self, self.prefix_current_title, self.remove_title_prefix)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        # Add main menu
        self.main_menu = MainMenu(self, self.main_frame, prefix_app_title=self.prefix_app_title)
        self.config(menu=self.main_menu)

    def start(self):
        self.mainloop()

    def prefix_app_title(self, prefix, separator=' - '):
        self.title(f'{prefix}{separator}{self.app_title}')

    def prefix_current_title(self, prefix, separator=' - ', replace=True):
        '''
        prefix: Prefix string
        separator: Separator string between prefix and title. Default is ' - '
        replace: Replace old prefix if True, prefix it otherwise. Default is True.
        '''
        # Get title
        # Cut prefix if replace is True
        title = self.title().replace(prefix, '', 1) if replace else self.title()
        self.title(f'{prefix}{separator}{title}')

    def remove_title_prefix(self, prefix):
        '''
        Remove `prefix` prefix from title
        '''
        title = self.title().replace(prefix, '', 1)
        self.title(title)
