import tkinter as tk
from tkinter import ttk, messagebox
from controller.instructor_controller import InstructorController

class StudentRosterView(tk.Toplevel):
    def __init__(self, root, section_id):
        super().__init__(root)
        self.section_id = section_id
        self.title(f"Student Roster - {section_id}")
        self.geometry("700x400")

        tk.Label(self, text=f"Students in {section_id}", font=("Arial", 12, "bold")).pack(pady=10)

        self.table = ttk.Treeview(
            self,
            columns=("studentID", "fullName", "email"),
            show="headings"
        )

        self.table.heading("studentID", text="Student ID")
        self.table.heading("fullName", text="Full Name")
        self.table.heading("email", text="Email")

        self.table.pack(fill=tk.BOTH, expand=True, padx=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Export Excel", command=lambda: self.export()).pack(side=tk.LEFT, padx=5)

        self.load_students()

    def load_students(self):
       
        students = InstructorController.get_students_by_section(self.section_id)

        for s in students:
            self.table.insert("", tk.END, values=(
                s["studentID"],
                s["fullName"],
                s["email"]
            ))

    def export(self):       
        success, path = InstructorController.export_roster(self.section_id)
       
        if success:
            messagebox.showinfo("Success", path)
        else:
            messagebox.showerror("Error", "Can not export!")
