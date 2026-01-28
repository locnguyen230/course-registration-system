import tkinter as tk
from tkinter import ttk, messagebox
from controller.admin_controller import AdminController


class AddAcademicConfigView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.title("Create Academic Configuration")
        self.geometry("480x360")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        # ===============================
        # TITLE
        # ===============================
        ttk.Label(
            self,
            text="Create Academic Configuration",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        # ===============================
        # FORM
        # ===============================
        form = ttk.Frame(self)
        form.pack(fill=tk.BOTH, expand=True, padx=20)

        # Academic Year
        ttk.Label(form, text="Academic Year (yyyy-yyyy)").grid(row=0, column=0, sticky="w", pady=5)
        self.year_entry = ttk.Entry(form, width=30)
        self.year_entry.grid(row=0, column=1, pady=5)

        # Semester
        ttk.Label(form, text="Semester").grid(row=1, column=0, sticky="w", pady=5)
        self.semester_cb = ttk.Combobox(
            form,
            values=["HK1", "HK2", "SUM"],
            state="readonly",
            width=28
        )
        self.semester_cb.grid(row=1, column=1, pady=5)
        self.semester_cb.current(0)

        # Policies
        ttk.Label(form, text="Policies").grid(row=2, column=0, sticky="nw", pady=5)
        self.policies_text = tk.Text(form, width=32, height=6)
        self.policies_text.grid(row=2, column=1, pady=5)

        # ===============================
        # BUTTONS
        # ===============================
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=15)

        ttk.Button(
            btn_frame,
            text="Save",
            width=15,
            command=self.save_config
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            btn_frame,
            text="Cancel",
            width=15,
            command=self.destroy
        ).grid(row=0, column=1, padx=5)

    # ===============================
    # SAVE
    # ===============================
    def save_config(self):
        academic_year = self.year_entry.get().strip()
        semester = self.semester_cb.get()
        policies = self.policies_text.get("1.0", tk.END).strip()

        if not academic_year or not semester:
            messagebox.showerror(
                "Error", "Academic Year and Semester are required"
            )
            return

        AdminController.create_academic_config(
            academic_year, semester, policies
        )

        messagebox.showinfo(
            "Success", "Academic configuration created successfully"
        )


        self.destroy()
