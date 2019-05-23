import tkinter as tk
from .find_entry import FindEntry

class FindFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()

    def post_init(self, editor):
        self.editor = editor
        self.find_entry.post_init(self.total_match_variable, self.find, self.see_previous_match, self.see_next_match, self.close)

    def create_widgets(self):
        self.find_entry = FindEntry(self)
        self.find_entry.pack(side=tk.LEFT)
        # Create find button
        self.find_button = tk.Button(self, text='Find', command=self.find)
        self.find_button.pack(side=tk.LEFT)
        # Create current match label
        self.current_match_variable = tk.IntVar(self)
        self.current_match_variable.set(0)
        self.current_match_label = tk.Label(self, textvariable=self.current_match_variable)
        self.current_match_label.pack(side=tk.LEFT)
        # Create separator label
        self.separator_label = tk.Label(self, text='/')
        self.separator_label.pack(side=tk.LEFT)
        # Create total match label
        self.total_match_variable = tk.IntVar(self)
        self.total_match_variable.set(0)
        self.total_match_label = tk.Label(self, textvariable=self.total_match_variable)
        self.total_match_label.pack(side=tk.LEFT)
        # Create previous match button
        self.previous_match_button = tk.Button(self, text='<', command=self.see_previous_match)
        self.previous_match_button.pack(side=tk.LEFT)
        # Create next match button
        self.next_match_button = tk.Button(self, text='>', command=self.see_next_match)
        self.next_match_button.pack(side=tk.LEFT)
        # Create close button
        self.close_button = tk.Button(self, text='X', command=self.close)
        self.close_button.pack(side=tk.LEFT)

    def clear_tags(self):
        self.editor.tag_delete('selected')
        self.editor.tag_delete('current_match')

    def see_match(self, index, length, order):
        self.editor.tag_delete('current_match')
        self.editor.tag_configure('current_match', background='gray', foreground='white')
        self.editor.tag_add('current_match', index, f'{index}+{length}c')
        self.editor.see(index)
        self.current_match_variable.set(order)

    def find(self, event=None):
        entry_text = self.find_entry.get()
        if entry_text:
            self.clear_tags()
            self.editor.tag_configure('selected', background='black', foreground='white')
            index = '1.0'
            self.count_var = tk.IntVar(self)
            self.total_match_variable.set(0)
            self.indices = []
            while index:
                index = self.editor.search(entry_text, index, count=self.count_var, nocase=True, stopindex=tk.END)
                if index:
                    self.total_match_variable.set(self.total_match_variable.get() + 1)
                    self.indices.append(index)
                    index = f'{index}+{self.count_var.get()}c'
            if self.indices:
                for index in self.indices:
                    self.editor.tag_add('selected', index, f'{index}+{self.count_var.get()}c')
                # See the first match
                self.see_match(self.indices[0], self.count_var.get(), 1)

    def see_previous_match(self, event=None):
        current_match_order = self.current_match_variable.get()
        if current_match_order:
            if current_match_order == 1:
                next_match_order = len(self.indices)
            else:
                next_match_order = current_match_order - 1
            self.see_match(self.indices[next_match_order-1], self.count_var.get(), next_match_order)

    def see_next_match(self, event=None):
        current_match_order = self.current_match_variable.get()
        if current_match_order:
            if current_match_order == len(self.indices):
                next_match_order = 1
            else:
                next_match_order = current_match_order + 1
            self.see_match(self.indices[next_match_order-1], self.count_var.get(), next_match_order)

    def close(self, event=None):
        self.current_match_variable.set(0)
        self.total_match_variable.set(0)
        self.place_forget()
        self.clear_tags()
        self.editor.focus_set()
