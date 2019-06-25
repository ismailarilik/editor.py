import tkinter as tk
import tkinter.filedialog as tkfiledialog
import tkinter.font as tkfont
import tkinter.messagebox as tkmessagebox
import io
import tokenize
from .file import File
from .find import FindView
from .highlight.tokenizer import Tokenizer

class Editor(tk.Text):
    def __init__(self, master, file, title, open_file, open_folder, search, set_tab_title, set_title, is_unsaved=False):
        super().__init__(master, undo=True, wrap=tk.NONE)
        self.file = file
        self.title = title
        self.open_file = open_file
        self.open_folder = open_folder
        self.search_command = search
        self.set_tab_title = set_tab_title
        self.set_title = set_title
        self.is_unsaved = is_unsaved

        self.tab_size = 4

        self.tokenizer = Tokenizer()
        self.token_type_color_map = self.get_token_type_color_map()

        self.find_view = None

        # Set a flag to ensure that opening file will not be behaved like a modification
        self.modified_event_triggered_by_opening_file = False
        # Set a flag to ensure modified callback being called only by a change
        self.modified_event_triggered_by_change = True

        self.add_key_bindings()
        # Listen for modified event
        self.bind('<<Modified>>', self.modified)

        # Open given file
        self.open()

    def add_key_bindings(self):
        # Prevent newline addition with '<Control-o>' and <Control-Shift-o> keys
        self.bind('<Control-o>', self.open_file_and_stop_propagation)
        self.bind('<Control-Shift-o>', self.open_folder_and_stop_propagation)
        # Prevent cursor movement with '<Control-f>', '<Control-F>', '<Control-Shift-f>' and '<Control-Shift-F>' keys
        self.bind('<Control-f>', self.find_and_stop_propagation)
        self.bind('<Control-F>', self.find_and_stop_propagation)
        self.bind('<Control-Shift-f>', self.search_and_stop_propagation)
        self.bind('<Control-Shift-F>', self.search_and_stop_propagation)
        # Escape from things in editor
        self.bind('<Escape>', self.escape)

    def close(self, event=None):
        '''
        Return True if the editor can be closed
        Return False otherwise
        '''
        # Before close, save unsaved changes
        return self.save_unsaved_changes(event)

    def close_find_view(self, event=None):
        self.find_view.close(event)
        self.find_view.place_forget()
        self.focus_set()

    def escape(self, event=None):
        '''
        Escape from things in editor
        '''
        # Close find view if it is opened
        if self.find_view and self.find_view.place_info():
            self.close_find_view(event)

    def find(self, event=None):
        # Create find view if it is not created yet
        if not self.find_view:
            self.find_view = FindView(self.master, self.close_find_view, self.search, self.see, self.tag_add, self.tag_configure, self.tag_delete)
        self.find_view.place(relx=1, anchor=tk.NE)
        self.find_view.find_entry.focus_set()
        self.find_view.find_entry.select_range(0, tk.END)

    def find_and_stop_propagation(self, event):
        self.find(event)
        return 'break'

    def get_token_type_color_map(self):
        return {
            Tokenizer.KEYWORD: '#FF0000',
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

    def get_wo_eol(self):
        '''
        Get without (automatically added) final end-of-line character
        '''
        return self.get('1.0', tk.END)[:-1]

    def highlight(self, event=None):
        if self.file.is_python_file:
            text = self.get('1.0', tk.END)
            if text:
                # Remove previous tags, otherwise they will conflict with new ones
                self.tag_delete(*self.tag_names())
                # Configure tag colors
                for token_type, token_color in self.token_type_color_map.items():
                    self.tag_config(self.tokenizer.get_token_name(token_type), foreground=token_color)
                # Tokenize and highlight
                tokens = self.tokenizer.tokenize(io.BytesIO(text.encode('UTF-8')).readline)
                while True:
                    try:
                        token = next(tokens)
                    except StopIteration:
                        break
                    except Exception as e:
                        pass
                    else:
                        # If there is a configured tag for this token, add it to the token's indices in the editor
                        color = self.token_type_color_map.get(token.exact_type)
                        if color:
                            start_index = f'{token.start_row}.{token.start_column}'
                            end_index = f'{token.end_row}.{token.end_column}'
                            self.tag_add(token.name, start_index, end_index)

    def modified(self, event):
        if self.modified_event_triggered_by_change:
            if not self.modified_event_triggered_by_opening_file:
                # Editor text is unsaved now, so set related flag
                # Also specify this state in title and tab title
                # Do them only if they were not set before, for a better performance
                if not self.is_unsaved:
                    self.is_unsaved = True
                    self.set_title(is_there_unsaved_change=True)
                    tab_index = str(self.master)
                    self.set_tab_title(tab_index, self.title, is_there_unsaved_change=True)
                else:
                    # If undo stack is empty, this means that there is no unsaved change
                    if not self.edit('canundo'):
                        # Update related flags, title and tab title
                        self.is_unsaved = False
                        self.set_title(is_there_unsaved_change=False)
                        tab_index = str(self.master)
                        self.set_tab_title(tab_index, self.title, is_there_unsaved_change=False)
            else:
                # Switch modified_event_triggered_by_opening_file flag off
                # Because the next modification will not be caused by opening a file
                self.modified_event_triggered_by_opening_file = False
                # Clear the undo and redo stacks.
                # Because, after opening file, these stacks should be empty.
                self.edit_reset()

            self.highlight(event)

            # Switch modified_event_triggered_by_change flag off
            # Because changing modified flag below causes modified event occurred again
            self.modified_event_triggered_by_change = False
            # Set modified flag to False so following modification may cause modified event occurred
            self.edit_modified(False)
        else:
            # Switch modified_event_triggered_by_change flag on
            # Because the next time modified event occurred will be caused by a change
            self.modified_event_triggered_by_change = True

    def open(self):
        '''
        Open given file
        '''
        with open(self.file.path, encoding='UTF-8') as file:
            file_text = file.read()
            if file_text:
                self.modified_event_triggered_by_opening_file = True
                self.insert(tk.END, file_text)

    def open_file_and_stop_propagation(self, event):
        self.open_file(event)
        return 'break'

    def open_folder_and_stop_propagation(self, event):
        self.open_folder(event)
        return 'break'

    def rename_file(self, new_file_path, event=None):
        self.file = File(new_file_path)
        self.set_title(file_name=self.file.name)
        tab_index = str(self.master)
        self.set_tab_title(tab_index, self.title, file_name=self.file.name)

    def save(self, event=None):
        with open(self.file.path, 'w', encoding='UTF-8') as file:
            file.write(self.get_wo_eol())
        self.is_unsaved = False
        # Insert a separator (boundary) on the undo stack.
        # This is necessary to separate undoing saved and unsaved changes.
        self.edit_separator()

    def save_as(self, event=None):
        # Get new file path
        file_name = self.file.name
        file_directory_path = self.file.directory_path
        file_extension = self.file.extension
        file_types = []
        if file_extension:
            if file_extension == '.py' or file_extension == '.pyw':
                file_types.append((_('Python Files'), file_extension))
            else:
                file_types.append((file_extension, file_extension))
        file_types.append((_('All Files'), '*'))
        file_path = tkfiledialog.asksaveasfilename(defaultextension=file_extension, filetypes=file_types, initialdir=file_directory_path, initialfile=file_name)

        if file_path:
            self.file = File(file_path)
            self.save(event)

    def save_unsaved_changes(self, event=None):
        '''
        Return True if unsaved changes were saved
        Return False otherwise
        '''
        if self.is_unsaved:
            message_box_title = _('Unsaved Changes')
            message_box_description = _('There are unsaved changes, would you like to save them?')
            user_reply = tkmessagebox.askyesnocancel(message_box_title, message_box_description)
            if user_reply:
                # Save unsaved changes
                self.save(event)
                return True
            elif user_reply == False:
                return True
            else:
                return False
        else:
            return True

    def search_and_stop_propagation(self, event):
        self.search_command(event)
        return 'break'

    @property
    def tab_size(self):
        return self._tab_size

    @tab_size.setter
    def tab_size(self, new_tab_size):
        self._tab_size = new_tab_size
        # Configure editor tab stops with specified tab size
        font = tkfont.Font(font=self['font'])
        tab_width = font.measure(' ' * self._tab_size)
        self.config(tabs=(tab_width,))
