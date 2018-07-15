import tkinter as tk

class App(object):
    def __init__(self):
        self.window = tk.Tk()
        # Set window title
        self.window.title('Visual Python')

    def start(self):
        self.window.mainloop()

app = App()
app.start()
