import tkinter as tk

class BaseView(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app   # app = controller
        self.pack(fill="both", expand=True)

    def destroy_view(self):
        self.destroy()