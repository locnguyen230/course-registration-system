import tkinter as tk
from tkinter import messagebox
from controller.auth_controller import AuthController

class ChangePasswordWindow(tk.Toplevel):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.title("Change Password")
        self.geometry("300x250")

        tk.Label(self, text="Current Password").pack()
        self.old_pw = tk.Entry(self, show="*")
        self.old_pw.pack()

        tk.Label(self, text="New Password").pack()
        self.new_pw = tk.Entry(self, show="*")
        self.new_pw.pack()

        tk.Button(self, text="Change",
                  command=self.handle_change).pack(pady=15)

    def handle_change(self):
        old = self.old_pw.get()
        new = self.new_pw.get()

        #  CALL CONTROLLER 
        success, msg = AuthController.change_password(
            self.user["userID"], old, new
        )

        if success:
            messagebox.showinfo(message = msg)
            self.destroy()
        else:
            messagebox.showerror(message= msg)
        

        