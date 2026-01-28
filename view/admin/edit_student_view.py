import tkinter as tk
from tkinter import ttk, messagebox
from controller.admin_controller import AdminController


class EditStudentView(tk.Toplevel):
    def __init__(self, parent, student_id):
        super().__init__(parent)

        self.student_id = student_id

        self.title("Edit Student")
        self.geometry("450x420")
        self.resizable(False, False)

        # call controller
        student = AdminController.get_info_edit(student_id)

       
        form = tk.Frame(self)
        form.pack(pady=15)

        tk.Label(form, text="Email").grid(row=2, column=0, sticky="e", pady=5)
        self.email_entry = tk.Entry(form, width=28)
        self.email_entry.insert(0, student["email"])
        self.email_entry.grid(row=2, column=1)

        tk.Label(form, text="Username").grid(row=0, column=0, sticky="e", pady=5)
        self.username_entry = tk.Entry(form, width=28)
        self.username_entry.insert(0, student["username"])
        self.username_entry.grid(row=0, column=1)

        tk.Label(form, text="Full Name").grid(row=1, column=0, sticky="e", pady=5)
        self.fullname_entry = tk.Entry(form, width=28)
        self.fullname_entry.insert(0, student["fullName"])
        self.fullname_entry.grid(row=1, column=1)

        tk.Label(form, text="New Password").grid(row=3, column=0, sticky="e", pady=5)
        self.password_entry = tk.Entry(form, width=28, show="*")
        self.password_entry.grid(row=3, column=1)


        tk.Label(form, text="Academic Status").grid(row=5, column=0, sticky="e", pady=5)
        self.academic_combo = ttk.Combobox(
            form,
            values=["ENROLLED", "SUSPENDED", "GRADUATED"],
            state="readonly",
            width=25
        )
        self.academic_combo.set(student["academicStatus"])
        self.academic_combo.grid(row=5, column=1)

        tk.Button(
            self,
            text="Update Student",
            width=18,
            command=self.update_student
        ).pack(pady=20)

    def update_student(self):
        userName = self.username_entry.get()
        fullname = self.fullname_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        academic_status = self.academic_combo.get()

        success = AdminController.update_student(
            self.student_id,
            userName,
            fullname,
            email,
            password,
            academic_status
        )

        if success:
            messagebox.showinfo(
                "Success",
                f"Student {self.student_id} updated"
            )
        else:
            messagebox.showerror(
                "Error",
                f"Student {self.student_id} can't updated"
            )
        self.destroy()
