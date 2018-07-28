import tkinter as tk
import tkinter.font as tk_font
import tkinter.filedialog as tk_filedialog
import tkinter.messagebox as tk_messagebox
import keyword
import tokenize
import enum
import io
import os

class Token(object):
    def __init__(self, type, exact_type, name, string, start_row, start_column, end_row, end_column, line):
        self.type = type
        self.exact_type = exact_type
        self.name = name
        self.string = string
        self.start_row = start_row
        self.start_column = start_column
        self.end_row = end_row
        self.end_column = end_column
        self.line = line

class Tokenizer(object):
    # Initialize keyword token type and name
    KEYWORD = 1000
    _KEYWORD_NAME = 'KEYWORD'

    def __init__(self):
        self._keywords = keyword.kwlist

    def get_token_name(self, token_type):
        if token_type == self.KEYWORD:
            return self._KEYWORD_NAME
        return tokenize.tok_name[token_type]

    def tokenize(self, readline):
        tokens = tokenize.tokenize(readline)
        for _token in tokens:
            token = Token(_token.type, _token.exact_type, tokenize.tok_name[_token.exact_type], _token.string, _token.start[0], _token.start[1], _token.end[0], _token.end[1], _token.line)
            # Check for keyword token
            if token.exact_type == tokenize.NAME and token.string in self._keywords:
                token.type = self.KEYWORD
                token.exact_type = token.type
                token.name = self._KEYWORD_NAME
            yield token

class Editor(tk.Text):
    # Initialize constants
    class TabType(enum.Enum):
        TAB = enum.auto()
        SPACE = enum.auto()

    def __init__(self, window):
        super().__init__(undo=True, wrap=tk.NONE)
        self.window = window
        # Initialize tab type and tab size properties
        self.tab_type = self.TabType.SPACE
        self.tab_size = 4
        self.tokenizer = Tokenizer()
        self.token_type_color_map = {
            self.tokenizer.KEYWORD: '#FF0000',
            tokenize.STRING: '#00C000',
            tokenize.NUMBER: '#0000FF',
            tokenize.COMMENT: '#808080',
            tokenize.LPAR: '#FFC000',
            tokenize.RPAR: '#FFC000',
            tokenize.LSQB: '#FF00FF',
            tokenize.RSQB: '#FF00FF',
            tokenize.LBRACE: '#00C0C0',
            tokenize.RBRACE: '#00C0C0',
            tokenize.EQUAL: '#800000',
            tokenize.PLUSEQUAL: '#800000',
            tokenize.MINEQUAL: '#800000',
            tokenize.STAREQUAL: '#800000',
            tokenize.DOUBLESTAREQUAL: '#800000',
            tokenize.SLASHEQUAL: '#800000',
            tokenize.DOUBLESLASHEQUAL: '#800000',
            tokenize.PERCENTEQUAL: '#800000',
            tokenize.ATEQUAL: '#800000',
            tokenize.VBAREQUAL: '#800000',
            tokenize.AMPEREQUAL: '#800000',
            tokenize.CIRCUMFLEXEQUAL: '#800000',
            tokenize.LEFTSHIFTEQUAL: '#800000',
            tokenize.RIGHTSHIFTEQUAL: '#800000',
            tokenize.PLUS: '#000080',
            tokenize.MINUS: '#000080',
            tokenize.STAR: '#000080',
            tokenize.DOUBLESTAR: '#000080',
            tokenize.SLASH: '#000080',
            tokenize.DOUBLESLASH: '#000080',
            tokenize.PERCENT: '#000080',
            tokenize.AT: '#000080',
            tokenize.VBAR: '#000080',
            tokenize.AMPER: '#000080',
            tokenize.TILDE: '#000080',
            tokenize.CIRCUMFLEX: '#000080',
            tokenize.LEFTSHIFT: '#000080',
            tokenize.RIGHTSHIFT: '#000080',
            tokenize.LESS: '#808000',
            tokenize.GREATER: '#808000',
            tokenize.EQEQUAL: '#808000',
            tokenize.NOTEQUAL: '#808000',
            tokenize.LESSEQUAL: '#808000',
            tokenize.GREATEREQUAL: '#808000',
            tokenize.DOT: '#800080',
            tokenize.COMMA: '#8000FF',
            tokenize.COLON: '#8080FF',
            tokenize.SEMI: '#FF0080',
            tokenize.RARROW: '#FF8080',
            tokenize.ELLIPSIS: '#FF80FF'
        }
        # Set vertical and horizontal scrollbars
        vertical_scrollbar = tk.Scrollbar(self.master)
        vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        vertical_scrollbar.config(command=self.yview)
        horizontal_scrollbar = tk.Scrollbar(self.master, orient=tk.HORIZONTAL)
        horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        horizontal_scrollbar.config(command=self.xview)
        self.config(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
        # Listen for Tab key press
        self.bind('<Tab>', self.on_press_tab)
        # Listen for Backspace key press
        self.bind('<BackSpace>', self.on_press_backspace)
        # Listen for Return key press
        self.bind('<Return>', self.on_press_return)
        # Set a flag to ensure modified callback being called only by a change
        self.modified_event_occurred_by_change = True
        # Listen for modified event
        self.bind('<<Modified>>', self.modified)
        # Handle open file event here, too for this widget and prevent propagation of event
        # Because default behavior of this widget is not wanted here
        self.bind('<Control-KeyPress-o>', self.handle_open_file_event_and_prevent_propagation)

    @property
    def tab_size(self):
        return self._tab_size

    @tab_size.setter
    def tab_size(self, new_tab_size):
        self._tab_size = new_tab_size
        # Also configure editor tab stops with specified tab size
        font = tk_font.Font(font=self['font'])
        tab_width = font.measure(' ' * self.tab_size)
        self.config(tabs=(tab_width,))

    def get_wo_eol(self):
        '''
        Get without (automatically added) final end-of-line character
        '''
        return self.get('1.0', tk.END)[:-1]

    def set(self, text):
        self.delete('1.0', tk.END)
        self.insert(tk.END, text)

    def _get_previous_tab_stop(self, index):
        '''
        Get previous tab stop for the case of which tab_type is SPACE
        '''
        row, col = index.split('.')
        if col == '0':
            return index
        excess_spaces = int(col) % self.tab_size
        previous_tab_stop_col = int(col) - (excess_spaces if excess_spaces != 0 else self.tab_size)
        return f'{row}.{previous_tab_stop_col}'

    def _get_next_tab_stop(self, index):
        '''
        Get next tab stop for the case of which tab_type is SPACE
        '''
        row, col = index.split('.')
        next_tab_stop_col = int(col) + (self.tab_size - int(col) % self.tab_size)
        return f'{row}.{next_tab_stop_col}'

    def _insert_indentation(self):
        '''
        Insert spaces up to next tab stop for the case of which tab_type is SPACE
        '''
        if self.tab_type is self.TabType.SPACE:
            index = self.index(tk.INSERT)
            row, col = index.split('.')
            next_tab_stop = self._get_next_tab_stop(self.index(tk.INSERT))
            next_tab_stop_row, next_tab_stop_col = next_tab_stop.split('.')
            space_count_to_insert = int(next_tab_stop_col) - int(col)
            self.insert(tk.INSERT, ' ' * space_count_to_insert)
            # Prevent additional tab character insertion by default handler
            return 'break'

    def on_press_tab(self, event):
        '''
        Insert spaces if `tab_type` equals to `TabType.SPACE`
        Allow default behavior which is inserting a tab character, otherwise
        The count of spaces which will be added, are determined by `tab_size`
        '''
        return self._insert_indentation()

    def on_press_backspace(self, event):
        '''
        If previous character is an indentation, delete it
        Otherwise, allow default behavior
        '''
        # Get text on the left
        row, col = self.index(tk.INSERT).split('.')
        left_text = self.get(f'{row}.0', tk.INSERT)
        # Check if left_text contains only space or tab characters
        # If this is not the case, allow default behavior
        left_text_space_and_tab_count = len(left_text) - len(left_text.strip(' \t'))
        if len(left_text) == left_text_space_and_tab_count:
            # Get left_text spaces on the right
            right_space_count = len(left_text) - len(left_text.rstrip(' '))
            # If the right space count is not zero, delete rightmost spaces to the indentation stop
            # Otherwise, allow default behavior
            if right_space_count != 0:
                previous_tab_stop = self._get_previous_tab_stop(self.index(tk.INSERT))
                self.delete(previous_tab_stop, tk.INSERT)
                # Prevent additional character removal by default handler
                return 'break'

    def on_press_return(self, event):
        '''
        First, insert an end-of-line character
        Then set indentation according to indentation of previous line
        If a `:` character exists at the end of previous line, it means this line is the first line of a block
        In this case, add one additional indentation
        Finally, prevent additional end-of-line character insertion by default handler
        '''
        self.insert(tk.INSERT, '\n')
        # Get previous line text
        row, col = self.index(tk.INSERT).split('.')
        previous_line_text = self.get(f'{int(row) - 1}.0', f'{row}.0')
        # Get indentation of previous line and insert it exactly to this line
        end_of_line_count = len(previous_line_text) - len(previous_line_text.lstrip(' \t'))
        previous_line_indentation_chars = previous_line_text[:end_of_line_count]
        self.insert(tk.INSERT, previous_line_indentation_chars)
        # If previous line ends with block starting `:` character, add one additional indentation
        try:
            if previous_line_text.rstrip()[-1] == ':':
                self._insert_indentation()
        except IndexError:
            pass
        # Prevent additional end-of-line character insertion by default handler
        return 'break'

    def modified(self, event):
        if self.modified_event_occurred_by_change:
            self.colorize()
            # Prefix current title with asterisk if it is not exist
            title = self.window.title()
            title = title if title.startswith('*') else f'*{title}'
            self.window.title(title)
            # Call this method to set modified flag to False so following modification may cause modified event occurred
            self.edit_modified(False)
        # Switch this flag, because changing modified flag above causes modified event occurred
        self.modified_event_occurred_by_change = not self.modified_event_occurred_by_change

    def colorize(self):
        # Remove previous tags, otherwise they will conflict with new ones
        self.tag_delete(*self.tag_names())
        # Configure tag colors
        for token_type, token_color in self.token_type_color_map.items():
            self.tag_config(self.tokenizer.get_token_name(token_type), foreground=token_color)
        text = self.get('1.0', tk.END)
        try:
            tokens = self.tokenizer.tokenize(io.BytesIO(text.encode('UTF-8')).readline)
            for token in tokens:
                # If there is a configured tag for this token, add it to the token's indices in the editor
                color = self.token_type_color_map.get(token.exact_type)
                if color:
                    start_index = f'{token.start_row}.{token.start_column}'
                    end_index = f'{token.end_row}.{token.end_column}'
                    self.tag_add(token.name, start_index, end_index)
        except:
            pass

    def handle_open_file_event_and_prevent_propagation(self, event):
        self.window.handle_open_file_event(event)
        return 'break'

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        # Initialize opened file path property
        self.opened_file_path = None
        # Set title
        self.title('<unsaved_file> - Visual Python')
        # Set icon
        self.iconbitmap('icon.ico')
        # Create menu
        self.menu = tk.Menu()
        self.config(menu=self.menu)
        # Create file menu
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Open File', accelerator='Ctrl+O', command=self.open_file)
        self.file_menu.add_command(label='Save File', accelerator='Ctrl+S', command=self.save_file)
        self.file_menu.add_command(label='Save File as...', accelerator='Ctrl+Shift+S', command=self.save_file_as)
        # Create editor
        self.editor = Editor(self)
        self.editor.pack(fill=tk.BOTH, expand=True)
        # Set window size as half of screen size
        # Also center window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = screen_width // 2
        window_height = screen_height // 2
        window_x = (screen_width // 2) - (window_width // 2)
        window_y = (screen_height // 2) - (window_height // 2)
        self.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')
        # Bind keyboard shortcuts
        # For open file
        self.bind('<Control-KeyPress-o>', self.handle_open_file_event)
        self.bind('<Control-KeyPress-O>', self.handle_open_file_event)
        # For save file
        self.bind('<Control-KeyPress-s>', self.handle_save_file_event)
        self.bind('<Control-KeyPress-S>', self.handle_save_file_event)
        # For save file as
        self.bind('<Control-Shift-KeyPress-s>', self.handle_save_file_as_event)
        self.bind('<Control-Shift-KeyPress-S>', self.handle_save_file_as_event)
        # Register delete window protocol to handle things properly on quit
        self.protocol('WM_DELETE_WINDOW', self.on_quit)
        # Start window
        self.mainloop()

    def handle_open_file_event(self, event):
        self.open_file()

    def handle_save_file_event(self, event):
        self.save_file()

    def handle_save_file_as_event(self, event):
        self.save_file_as()

    def open_file(self):
        opened_file_path = tk_filedialog.askopenfilename(filetypes=[('Python Files', '.py')])
        if opened_file_path:
            self.opened_file_path = opened_file_path
            # Set editor text with file content
            with tokenize.open(self.opened_file_path) as file:
                self.editor.set(file.read())
            # Prefix window title with opened file name
            opened_file_name = os.path.basename(self.opened_file_path)
            self.title(f'{opened_file_name} - Visual Python')

    def save_file(self):
        # If a file was not opened before, call save_file_as method
        # Else, write editor text to the file
        if not self.opened_file_path:
            self.save_file_as()
        else:
            with open(self.opened_file_path, 'w', encoding='UTF-8') as file:
                file.write(self.editor.get_wo_eol())
            # Prefix window title with opened file name
            opened_file_name = os.path.basename(self.opened_file_path)
            self.title(f'{opened_file_name} - Visual Python')

    def save_file_as(self):
        opened_file_path = tk_filedialog.asksaveasfilename(defaultextension='.py', filetypes=[('Python Files', '.py')])
        if opened_file_path:
            self.opened_file_path = opened_file_path
            with open(self.opened_file_path, 'w', encoding='UTF-8') as file:
                file.write(self.editor.get_wo_eol())
            # Prefix window title with opened file name
            opened_file_name = os.path.basename(self.opened_file_path)
            self.title(f'{opened_file_name} - Visual Python')

    def on_quit(self):
        # If there are unsaved changes, warn user about that
        # Otherwise, destroy the app as usual
        if self.title().startswith('*'):
            reply= tk_messagebox.askyesnocancel('Unsaved Changes', 'There are unsaved changes, would you like to save them?')
            # If user choose to save, save the file and destroy the app
            # If user choose not to save, just destroy the app
            # If user cancel quitting, do nothing
            if reply:
                self.save_file()
                self.destroy()
            elif reply == False:
                self.destroy()
            else:
                pass
        else:
            self.destroy()

if __name__ == '__main__':
    Window()