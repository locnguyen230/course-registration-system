import tkinter as tk
from tkinter import ttk, messagebox
from controller.admin_controller import AdminController


class EditPrerequisiteView(tk.Toplevel):
    def __init__(self, parent, course_id):
        super().__init__(parent)

        self.course_id = course_id

        self.title("Edit Prerequisites")
        self.geometry("420x230")
        self.resizable(False, False)

        self.create_widgets()
        self.load_prerequisites()

    # ===============================
    # UI
    # ===============================
    def create_widgets(self):
        ttk.Label(
            self,
            text=f"Edit Prerequisites for {self.course_id}",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        form = ttk.Frame(self)
        form.pack(padx=20, pady=10, fill=tk.X)

        ttk.Label(
            form,
            text="Prerequisite IDs (comma separated)"
        ).grid(row=0, column=0, sticky="w", pady=5)

        self.prereq_entry = ttk.Entry(form, width=40)
        self.prereq_entry.grid(row=1, column=0, pady=5)

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=15)

        ttk.Button(
            btn_frame,
            text="Save",
            width=14,
            command=self.save_prerequisites
        ).grid(row=0, column=0, padx=6)

        ttk.Button(
            btn_frame,
            text="Cancel",
            width=14,
            command=self.destroy
        ).grid(row=0, column=1, padx=6)

    # ===============================
    # LOAD DATA
    # ===============================
    def load_prerequisites(self):
        prereqs = AdminController.get_prerequisites_by_course(self.course_id)

        prereq_text = ", ".join(prereqs) if prereqs else ""
        self.prereq_entry.insert(0, prereq_text)

    # ===============================
    # SAVE
    # ===============================
    def save_prerequisites(self):
        prereq_text = self.prereq_entry.get().strip()

        success, msg = AdminController.edit_prerequisites(
            self.course_id,
            prereq_text
        )

        if success:
            messagebox.showinfo("Success", msg)
            self.destroy()
        else:
            messagebox.showerror("Error", msg)
