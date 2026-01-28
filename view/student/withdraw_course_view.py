import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from controller.student_controller import StudentController

class WithdrawCourseWindow(tk.Toplevel):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.title("Withdraw Course")
        self.geometry("500x300")

        tk.Label(self, text="Registered Courses", font=("Arial", 12, "bold")).pack(pady=5)

 
        columns = ( "sectionID", "courseName", "registrationDate")

        self.table = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=8
        )

        self.table.heading("sectionID", text="Course Code")
        self.table.heading("courseName", text="Course Name")
        self.table.heading("registrationDate", text="Register Date")

        self.table.column("sectionID", width=120, anchor="center")
        self.table.column("courseName", width=220)
        self.table.column("registrationDate", width=120, anchor="center")

        self.table.pack(fill="both", expand=True, padx=10, pady=10)

   
        self.load_registered_courses()

        tk.Button(
            self,
            text="Withdraw",
            command=self.handle_withdraw,
            bg="#d9534f",
            fg="white"
        ).pack(pady=10)

    def load_registered_courses(self):
        
        demo_data = StudentController.get_registrationrecord(
            self.user["studentID"]
        )

        for row in demo_data:
            self.table.insert("", "end", values=row)

    def handle_withdraw(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a course"
            )
            return

        item_id = selected[0]

        values = self.table.item(item_id, "values")

        section_id = values[0]
        course_id = values[1]
        course_name = values[2]

        confirm = messagebox.askyesno(
            "Confirm Withdraw",
            f"Withdraw course:\n{course_id} - {course_name}?"
        )
        if not confirm:
            return

        success = StudentController.withdraw_course(
            self.user["studentID"],
            section_id
        )

        if success:
            messagebox.showinfo("Success", "Withdraw Success")
            self.load_registered_courses()  
        else:
            messagebox.showerror("Error", "Withdrawal unsuccessful")