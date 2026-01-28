import tkinter as tk
from tkinter import ttk, messagebox
from controller.admin_controller import AdminController


class EditAcademicConfigView(tk.Toplevel):
    def __init__(self, parent, config_id):
        super().__init__(parent)

        self.parent = parent
        self.config_id = config_id

        self.title("Edit Academic Configuration")
        self.geometry("480x360")
        self.resizable(False, False)

        self.create_widgets()
        self.load_config_data()

    # ===============================
    # UI
    # ===============================
    def create_widgets(self):
        ttk.Label(
            self,
            text="Edit Academic Configuration",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        form = ttk.Frame(self)
        form.pack(fill=tk.BOTH, expand=True, padx=20)

        # Config ID (readonly)
        ttk.Label(form, text="Config ID").grid(row=0, column=0, sticky="w", pady=5)
        self.config_id_entry = ttk.Entry(form, width=30, state="readonly")
        self.config_id_entry.grid(row=0, column=1, pady=5)

        # Academic Year
        ttk.Label(form, text="Academic Year (yyyy-yyyy)").grid(row=1, column=0, sticky="w", pady=5)
        self.year_entry = ttk.Entry(form, width=30)
        self.year_entry.grid(row=1, column=1, pady=5)

        # Semester
        ttk.Label(form, text="Semester").grid(row=2, column=0, sticky="w", pady=5)
        self.semester_cb = ttk.Combobox(
            form,
            values=["HK1", "HK2", "SUM"],
            state="readonly",
            width=28
        )
        self.semester_cb.grid(row=2, column=1, pady=5)

        # Policies
        ttk.Label(form, text="Policies").grid(row=3, column=0, sticky="nw", pady=5)
        self.policies_text = tk.Text(form, width=32, height=6)
        self.policies_text.grid(row=3, column=1, pady=5)

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=15)

        ttk.Button(
            btn_frame,
            text="Update",
            width=15,
            command=self.update_config
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            btn_frame,
            text="Cancel",
            width=15,
            command=self.destroy
        ).grid(row=0, column=1, padx=5)

    # ===============================
    # LOAD DATA
    # ===============================
    def load_config_data(self):
        config = AdminController.get_academic_config_by_id(self.config_id)

        if not config:
            messagebox.showerror(
                "Error", "Academic configuration not found"
            )
            self.destroy()
            return

        self.config_id_entry.config(state="normal")
        self.config_id_entry.insert(0, config["configID"])
        self.config_id_entry.config(state="readonly")

        self.year_entry.insert(0, config["academicYear"])
        self.semester_cb.set(config["semester"])

        self.policies_text.insert("1.0", config["policies"])

    # ===============================
    # UPDATE
    # ===============================
    def update_config(self):
        academic_year = self.year_entry.get().strip()
        semester = self.semester_cb.get()
        policies = self.policies_text.get("1.0", tk.END).strip()

        if not academic_year or not semester:
            messagebox.showerror(
                "Error", "Academic Year and Semester are required"
            )
            return

        success = AdminController.update_config_by_id(
            self.config_id,
            academic_year,
            semester,
            policies
        )

        if success:
            messagebox.showinfo(
                "Success", "Academic configuration updated successfully"
            )

            self.destroy()
        else:
            messagebox.showerror(
                "Error", "Update failed"
            )
