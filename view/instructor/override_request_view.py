import tkinter as tk
from tkinter import ttk, messagebox
from controller.instructor_controller import InstructorController


class OverrideRequestView(tk.Toplevel):
    def __init__(self, root, instructor_id):
        super().__init__(root)
        self.instructor_id = instructor_id

        self.title("Override Requests")
        self.geometry("900x420")

        tk.Label(
            self,
            text="Override / Waitlist Requests",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        # ===============================
        # TABLE
        # ===============================
        columns = (
            "waitlistID",
            "studentID",
            "fullName",
            "email",
            "sectionID",
            "status"
        )

        self.table = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=10
        )

        self.table.heading("waitlistID", text="Request ID")
        self.table.heading("studentID", text="Student ID")
        self.table.heading("fullName", text="Full Name")
        self.table.heading("email", text="Email")
        self.table.heading("sectionID", text="Section")
        self.table.heading("status", text="Status")

        self.table.column("waitlistID", width=90, anchor="center")
        self.table.column("studentID", width=120, anchor="center")
        self.table.column("fullName", width=160)
        self.table.column("email", width=200)
        self.table.column("sectionID", width=130, anchor="center")
        self.table.column("status", width=90, anchor="center")

        self.table.pack(fill=tk.BOTH, expand=True, padx=10)

        # ===============================
        # BUTTONS
        # ===============================
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Approve",
            width=12,
            command=lambda: self.update_status("APPROVED")
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="Reject",
            width=12,
            command=lambda: self.update_status("REMOVED")
        ).pack(side=tk.LEFT, padx=5)

        self.load_requests()

    # ==================================================
    # LOAD WAITLIST / OVERRIDE REQUESTS
    # ==================================================
    def load_requests(self):
        self.table.delete(*self.table.get_children())

        requests = InstructorController.get_override_requests(
            self.instructor_id
        )

        for r in requests:
            self.table.insert(
                "",
                tk.END,
                values=(
                    r["waitlistID"],
                    r["studentID"],
                    r["fullName"],
                    r["email"],
                    r["sectionID"],
                    r["status"]
                )
            )

    # ==================================================
    # APPROVE / REJECT
    # ==================================================
    def update_status(self, status):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a request"
            )
            return

        values = self.table.item(selected[0])["values"]

        waitlist_id = values[0] 

        success, msg = InstructorController.process_override(
            waitlist_id,
            status
        )

        if success:
            messagebox.showinfo("Success", msg)
            self.load_requests()
        else:
            messagebox.showerror("Error", msg)
