import tkinter as tk

class StudentDashboard(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.title("Student Dashboard")
        self.geometry("400x300")

        tk.Label(self, text="Welcome Student", font=("Arial", 14)).pack(pady=10)

        tk.Button(self, text="Register Course",
                  command=self.open_register).pack(fill="x", padx=50, pady=5)

        tk.Button(self, text="Withdraw Course",
                  command=self.open_withdraw).pack(fill="x", padx=50, pady=5)

        tk.Button(self, text="View Waitlist",
                  command=self.open_waitlist).pack(fill="x", padx=50, pady=5)

        tk.Button(self, text="Change Password",
                  command=self.open_change_password).pack(fill="x", padx=50, pady=5)

    def open_register(self):
        from view.student.register_course_view import RegisterCourseWindow
        RegisterCourseWindow(self, self.user)

    def open_withdraw(self):
        from view.student.withdraw_course_view import WithdrawCourseWindow
        WithdrawCourseWindow(self, self.user)

    def open_waitlist(self):
        from view.student.waitlist_status_view import WaitlistWindow
        WaitlistWindow(self, self.user)

    def open_change_password(self):
        from view.common.change_password_view import ChangePasswordWindow
        ChangePasswordWindow(self, self.user)
