import tkinter as tk
from tkinter import ttk, messagebox
from controller.admin_controller import AdminController


class AddPrerequisiteView(tk.Toplevel):
    def __init__(self, parent, course_id):
        super().__init__(parent)

        self.course_id = course_id

        self.title("Add Prerequisite")
        self.geometry("380x220")
        self.resizable(False, False)

        self.create_widgets()

  
    def create_widgets(self):
        ttk.Label(
            self,
            text="Add Prerequisite Course",
            font=("Arial", 13, "bold")
        ).pack(pady=10)

        form = ttk.Frame(self)
        form.pack(padx=20, pady=10, fill=tk.X)

        # Course ID (readonly)
        ttk.Label(form, text="Course ID").grid(row=0, column=0, sticky="w", pady=6)
        self.course_entry = ttk.Entry(form, width=30, state="readonly")
        self.course_entry.grid(row=0, column=1, pady=6)
        self.course_entry.config(state="normal")
        self.course_entry.insert(0, self.course_id)
        self.course_entry.config(state="readonly")

        # Prerequisite ID (input)
        ttk.Label(form, text="Prerequisite ID (IT1001,IT1002)").grid(row=1, column=0, sticky="w", pady=6)
        self.prereq_entry = ttk.Entry(form, width=30)
        self.prereq_entry.grid(row=1, column=1, pady=6)

  
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=15)

        ttk.Button(
            btn_frame,
            text="Add",
            width=14,
            command=self.add_prerequisite
        ).grid(row=0, column=0, padx=6)

        ttk.Button(
            btn_frame,
            text="Cancel",
            width=14,
            command=self.destroy
        ).grid(row=0, column=1, padx=6)

   
    def add_prerequisite(self):
        prereq_id = self.prereq_entry.get().strip()

        if not prereq_id:
            messagebox.showerror(
                "Error",
                "Prerequisite ID is required"
            )
            return

        if prereq_id == self.course_id:
            messagebox.showerror(
                "Error",
                "A course cannot be its own prerequisite"
            )
            return

        success, result= AdminController.add_prerequisite(
            self.course_id,
            prereq_id
        )

        if success:
            messagebox.showinfo(
                "Success",
                result
            )
            self.destroy()
        else:
            messagebox.showerror(
                "Error",
                "Failed to add prerequisite"
            )
