import tkinter as tk
from tkinter import ttk, messagebox
from controller.admin_controller import AdminController


class ManageStudentView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Manage Students")
        self.geometry("850x450")


        columns = ("studentID", "username", "fullName")

        self.student_table = ttk.Treeview(
            self, columns=columns, show="headings", height=12
        )

        self.student_table.heading("studentID", text="Student ID")
        self.student_table.heading("username", text="Username")
        self.student_table.heading("fullName", text="Full Name")

        self.student_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.load_students()

   
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame, text="Add Student", width=15,
            command=self.open_add_student
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame, text="Edit Student", width=15,
            command=self.edit_student
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame, text="Delete Student", width=15,
            command=self.delete_student
        ).grid(row=0, column=2, padx=5)


    def load_students(self):
        self.student_table.delete(*self.student_table.get_children())

        students = AdminController.get_list_student()

        for s in students:
            self.student_table.insert(
                "", "end",
                values=(s["studentID"], s["username"], s["fullName"])
            )

  
    def open_add_student(self):
        from view.admin.add_student_view import AddStudentView
        AddStudentView(self).mainloop()

 
    def edit_student(self):
        selected = self.student_table.selection()
        if not selected:
            messagebox.showwarning(
                "Warning", "Please select a student to edit"
            )
            return

        student_id = self.student_table.item(selected[0])["values"][0]

        from view.admin.edit_student_view import EditStudentView
        EditStudentView(self, student_id)

  
    def delete_student(self):
        selected = self.student_table.selection()
        if not selected:
            messagebox.showwarning(
                "Warning", "Please select a student to delete"
            )
            return

        student_id = self.student_table.item(selected[0])["values"][0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete student {student_id}?"
        )

        if confirm:
            success = AdminController.delete_student(student_id)
            if success:
                messagebox.showinfo( "Deleted", f"Student {student_id} deleted")
            else:
                messagebox.showerror( "Deleted", f"Student {student_id} deleted faild")
            self.load_students()
