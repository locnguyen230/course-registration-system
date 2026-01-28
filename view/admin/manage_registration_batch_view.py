import tkinter as tk
from tkinter import ttk, messagebox
from controller.admin_controller import AdminController


class ManageRegistrationBatchView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Manage Registration Batches")
        self.geometry("1050x450")

        # ===============================
        # BATCH TABLE
        # ===============================
        columns = (
            "batchID",
            "semester",
            "startTime",
            "endTime",
            "eligibleYearLevel"
        )

        self.batch_table = ttk.Treeview(
            self, columns=columns, show="headings", height=12
        )

        self.batch_table.heading("batchID", text="Batch ID")
        self.batch_table.heading("semester", text="Semester")
        self.batch_table.heading("startTime", text="Start Time")
        self.batch_table.heading("endTime", text="End Time")
        self.batch_table.heading("eligibleYearLevel", text="Eligible Year Level")

        self.batch_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.load_batches()

        # ===============================
        # ACTION BUTTONS
        # ===============================
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame, text="Create Batch", width=18,
            command=self.open_create_batch
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame, text="Edit Batch", width=18,
            command=self.edit_batch
        ).grid(row=0, column=1, padx=5)

    # ===============================
    # LOAD BATCH LIST (DEMO DATA)
    # ===============================
    def load_batches(self):
        self.batch_table.delete(*self.batch_table.get_children())

        # 🔥 DEMO DATA
        # Sau này thay bằng:
        batches = AdminController.get_registration_batches()


        for b in batches:
            self.batch_table.insert(
                "",
                "end",
                values=(
                    b["batchID"],
                    b["semester"],
                    b["startTime"],
                    b["endTime"],
                    b["eligibleYearLevel"]
                )
            )

    # ===============================
    # CREATE BATCH
    # ===============================
    def open_create_batch(self):
        from view.admin.add_registrationbatch_view import AddRegistrationBatchView
        AddRegistrationBatchView(self)
        

    # ===============================
    # EDIT BATCH
    # ===============================
    def edit_batch(self):
        selected = self.batch_table.selection()
        if not selected:
            messagebox.showwarning(
                "Warning", "Please select a batch to edit"
            )
            return

        batch_id = self.batch_table.item(selected[0])["values"][0]

        from view.admin.edit_registrationbatch_view import EditRegistrationBatchView
        EditRegistrationBatchView(self, batch_id)
        
