import tkinter as tk
from tkinter import ttk, messagebox
from controller.student_controller import StudentController

class StudentDashboard(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.title("Student Dashboard")
        self.geometry("1000x400")

        tk.Label(self, text="Welcome Student", font=("Arial", 14)).pack(pady=5)

        # UC-S2 – SEARCH COURSE
        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(search_frame, text="Search (Major Code):").pack(side="left")
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="Search",
            command=self.search_course
        ).pack(side="left")

        # UC-S1 – VIEW COURSE LIST
        columns = ("courseID", "courseName", "credits", "available")
        self.course_table = ttk.Treeview(
            self, columns=columns, show="headings", height=8
        )

        self.course_table.heading("courseID", text="Course")
        self.course_table.heading("courseName", text="Course Name")
        self.course_table.heading("credits", text="Credits")
        self.course_table.heading("available", text="Available Slots")

        self.course_table.pack(fill="both", expand=True, padx=10, pady=5)

        self.load_course_list()

       
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Register Course",
                  command=self.open_register).grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="Withdraw Course",
                  command=self.open_withdraw).grid(row=0, column=1, padx=5)

        tk.Button(btn_frame, text="View Waitlist",
                  command=self.open_waitlist).grid(row=0, column=2, padx=5)

        tk.Button(btn_frame, text="Change Password",
                  command=self.open_change_password).grid(row=0, column=3, padx=5)

   
    # UC-S1 – VIEW COURSE LIST
    def load_course_list(self):
        self.course_table.delete(*self.course_table.get_children())

    
        courses = StudentController.view_course_list()

      
        for c in courses:
            self.course_table.insert(
                "", "end",
                values=(c["courseID"], c["courseName"], c["credits"], c["available"])
            )

    # UC-S2 – SEARCH COURSE
    def search_course(self):
        keyword = self.search_entry.get().strip()

        self.course_table.delete(*self.course_table.get_children())

        # Nếu không nhập gì → quay lại UC-S1
        if keyword == "":
            courses = StudentController.view_course_list()
        else:
            courses = StudentController.search_course(keyword)

        for c in courses:
            self.course_table.insert(
                "",
                "end",
                values=(
                    c["courseID"],
                    c["courseName"],
                    c["credits"],
                    c["available"]
                )
            )


    # CÁC HÀM CŨ – GIỮ NGUYÊN
    def open_register(self):
        from controller.student_controller import StudentController
        from view.student.register_course_view import RegisterCourseWindow
        from tkinter import messagebox

        success, time, batch_id= StudentController.check_registrationbatch(
            self.user["studentID"]
        )

        if not success:
            messagebox.showwarning(time)
            return

        RegisterCourseWindow(self, self.user, time, batch_id)


    def open_withdraw(self):
        from view.student.withdraw_course_view import WithdrawCourseWindow
        WithdrawCourseWindow(self, self.user)

    def open_waitlist(self):
        from view.student.waitlist_status_view import WaitlistWindow
        WaitlistWindow(self, self.user)

    def open_change_password(self):
        from view.common.change_password_view import ChangePasswordWindow
        ChangePasswordWindow(self, self.user)
