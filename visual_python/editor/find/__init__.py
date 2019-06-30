import tkinter as tk
import tkinter.ttk as ttk
import os.path

class FindView(ttk.Frame):
    def __init__(self, master, close_find_view, editor_search, editor_see, editor_tag_add, editor_tag_configure, editor_tag_delete):
        super().__init__(master)
        self.close_find_view = close_find_view
        self.editor_search = editor_search
        self.editor_see = editor_see
        self.editor_tag_add = editor_tag_add
        self.editor_tag_configure = editor_tag_configure
        self.editor_tag_delete = editor_tag_delete
        self.create_widgets()
        self.add_key_bindings()
    
    def add_key_bindings(self, event=None):
        # Add key bindings for the find entry
        self.find_entry.bind('<Return>', self.find_or_see_next_match)
        self.find_entry.bind('<Shift-Return>', self.see_previous_match)
        self.find_entry.bind('<Escape>', self.close_find_view)
    
    def clear_entry(self, event=None):
        self.find_entry.delete(0, tk.END)
    
    def clear_tags(self, event=None):
        self.editor_tag_delete('match')
        self.editor_tag_delete('current_match')
    
    def close(self, event=None):
        self.current_match_variable.set(0)
        self.total_match_variable.set(0)
        self.clear_tags()
    
    def create_widgets(self, event=None):
        current_directory = os.path.dirname(__file__)
        
        self.find_entry = ttk.Entry(self)
        self.find_entry.pack(side=tk.LEFT)
        
        # Create find button
        find_button_image_path = os.path.join(current_directory, '../../icons/find_icons/find.png')
        self.find_button_image = tk.PhotoImage(file=find_button_image_path)
        self.find_button = ttk.Button(self, image=self.find_button_image, command=self.find)
        self.find_button.pack(side=tk.LEFT)
        
        # Create current match label
        self.current_match_variable = tk.IntVar()
        self.current_match_variable.set(0)
        self.current_match_label = ttk.Label(self, textvariable=self.current_match_variable)
        self.current_match_label.pack(side=tk.LEFT)
        
        self.separator_label = ttk.Label(self, text='/')
        self.separator_label.pack(side=tk.LEFT)
        
        # Create total match label
        self.total_match_variable = tk.IntVar()
        self.total_match_variable.set(0)
        self.total_match_label = ttk.Label(self, textvariable=self.total_match_variable)
        self.total_match_label.pack(side=tk.LEFT)
        
        # Create previous match button
        previous_match_button_image_path = os.path.join(current_directory, '../../icons/find_icons/previous.png')
        self.previous_match_button_image = tk.PhotoImage(file=previous_match_button_image_path)
        self.previous_match_button = ttk.Button(self, image=self.previous_match_button_image, command=self.see_previous_match)
        self.previous_match_button.pack(side=tk.LEFT)
        
        # Create next match button
        next_match_button_image_path = os.path.join(current_directory, '../../icons/find_icons/next.png')
        self.next_match_button_image = tk.PhotoImage(file=next_match_button_image_path)
        self.next_match_button = ttk.Button(self, image=self.next_match_button_image, command=self.see_next_match)
        self.next_match_button.pack(side=tk.LEFT)
        
        # Create close button
        close_button_image_path = os.path.join(current_directory, '../../icons/find_icons/close.png')
        self.close_button_image = tk.PhotoImage(file=close_button_image_path)
        self.close_button = ttk.Button(self, image=self.close_button_image, command=self.close_find_view)
        self.close_button.pack(side=tk.LEFT)
    
    def find(self, event=None):
        entry_text = self.find_entry.get()
        if entry_text:
            self.clear_tags()
            self.editor_tag_configure('match', background='black', foreground='white')
            index = '1.0'
            self.match_size_variable = tk.IntVar()
            self.total_match_variable.set(0)
            self.indices = []
            while index:
                index = self.editor_search(entry_text, index, count=self.match_size_variable, nocase=True, stopindex=tk.END)
                if index:
                    self.total_match_variable.set(self.total_match_variable.get() + 1)
                    self.indices.append(index)
                    index = f'{index}+{self.match_size_variable.get()}c'
            if self.indices:
                for index in self.indices:
                    self.editor_tag_add('match', index, f'{index}+{self.match_size_variable.get()}c')
                # See the first match
                self.see_match(self.indices[0], self.match_size_variable.get(), 1)
    
    def find_or_see_next_match(self, event=None):
        if not self.total_match_variable.get():
            self.find(event=event)
        else:
            self.see_next_match(event=event)
    
    def see_match(self, index, length, match_index, event=None):
        self.editor_tag_delete('current_match')
        self.editor_tag_configure('current_match', background='gray', foreground='white')
        self.editor_tag_add('current_match', index, f'{index}+{length}c')
        self.editor_see(index)
        self.current_match_variable.set(match_index)
    
    def see_next_match(self, event=None):
        current_match_index = self.current_match_variable.get()
        if current_match_index:
            if current_match_index == len(self.indices):
                next_match_index = 1
            else:
                next_match_index = current_match_index + 1
            self.see_match(self.indices[next_match_index-1], self.match_size_variable.get(), next_match_index)
    
    def see_previous_match(self, event=None):
        current_match_index = self.current_match_variable.get()
        if current_match_index:
            if current_match_index == 1:
                previous_match_index = len(self.indices)
            else:
                previous_match_index = current_match_index - 1
            self.see_match(self.indices[previous_match_index-1], self.match_size_variable.get(), previous_match_index)