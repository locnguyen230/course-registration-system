import tkinter as tk
from tkinter import ttk, messagebox
from controller.admin_controller import AdminController


class AcademicConfigView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Configure Academic Information")
        self.geometry("1000x420")

        # ===============================
        # ACADEMIC CONFIG TABLE
        # ===============================
        columns = (
            "configID",
            "academicYear",
            "semester",
            "policies"
        )

        self.academic_table = ttk.Treeview(
            self, columns=columns, show="headings", height=12
        )

        self.academic_table.heading("configID", text="Config ID")
        self.academic_table.heading("academicYear", text="Academic Year")
        self.academic_table.heading("semester", text="Semester")
        self.academic_table.heading("policies", text="Policies")

        self.academic_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Load data
        self.load_academic_configs()

        # ===============================
        # ACTION BUTTONS
        # ===============================
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Create Config",
            width=18,
            command=self.open_create_config
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Update Config",
            width=18,
            command=self.open_update_config
        ).grid(row=0, column=1, padx=5)

    # ===============================
    # LOAD CONFIG LIST
    # ===============================
    def load_academic_configs(self):
        self.academic_table.delete(*self.academic_table.get_children())

        configs = AdminController.get_academic_configs()

        for c in configs:
            self.academic_table.insert(
                "",
                "end",
                values=(
                    c["configID"],
                    c["academicYear"],
                    c["semester"],
                    c["policies"]
                )
            )

    # ===============================
    # CREATE
    # ===============================
    def open_create_config(self):
        from view.admin.add_new_config_view import AddAcademicConfigView
        AddAcademicConfigView(self)

    # ===============================
    # UPDATE
    # ===============================
    def open_update_config(self):
        selected = self.academic_table.selection()
        if not selected:
            messagebox.showwarning(
                "Warning", "Please select a config to update"
            )
            return

        config_id = self.academic_table.item(selected[0])["values"][0]

        from view.admin.edit_config_view import EditAcademicConfigView
        EditAcademicConfigView(self, config_id)
