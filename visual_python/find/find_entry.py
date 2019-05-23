import tkinter as tk

class FindEntry(tk.Entry):
    def __init__(self, master, get_total_match_variable_value, find, see_previous_match, see_next_match, close_find_frame):
        super().__init__(master)
        self.get_total_match_variable_value = get_total_match_variable_value
        self.find = find
        self.see_previous_match = see_previous_match
        self.see_next_match = see_next_match
        self.close_find_frame = close_find_frame

        self.add_keyboard_bindings()

    def clear(self):
        self.delete(0, tk.END)

    def add_keyboard_bindings(self):
        self.bind('<Return>', self.find_or_see_next_match)
        self.bind('<Shift-Return>', self.see_previous_match)
        # Add Escape keyboard binding for closing find frame
        self.bind('<Escape>', self.close_find_frame)

    def find_or_see_next_match(self, event=None):
        if not self.get_total_match_variable_value():
            self.find(event)
        else:
            self.see_next_match(event)
