import tkinter as tk
from tkinter import messagebox
from controller.auth_controller import AuthController

class LoginView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Login")
        self.geometry("300x200")

        tk.Label(self, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Login", command=self.handle_login).pack(pady=15)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # 🔥 CALL CONTROLLER HERE
        success, result = AuthController.authenticate(username, password)

  
        if not success:
            messagebox.showerror(message=result)
            return

        self.destroy()

        role = result["role"]

        if role == "STUDENT":
            from view.student.student_dashboard import StudentDashboard
            StudentDashboard(result).mainloop()

        elif role == "INSTRUCTOR":
            from view.instructor.instructor_dashboard import InstructorDashboard
            InstructorDashboard(result).mainloop()

        elif role == "ADMIN":
            from view.admin.admin_dashboard import AdminDashboard
            AdminDashboard(result).mainloop()

        else:
            messagebox.showerror(message="Unknown user role")