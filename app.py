import tkinter as tk

class App(object):
    def __init__(self):
        self.window = tk.Tk()

    def start(self):
        self.window.mainloop()

app = App()
app.start()
