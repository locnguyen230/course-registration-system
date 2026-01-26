import tkinter as tk
from tkinter import ttk
from controller.student_controller import StudentController


class WaitlistWindow(tk.Toplevel):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user

        self.title("Waitlist Status")
        self.geometry("650x320")

        tk.Label(
            self,
            text="Your Waitlist Status",
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        # ===============================
        # TABLE (WAITLIST)
        # ===============================
        columns = (
            "sectionID",
            "courseID",
            "courseName",
            "status",
            "position"
        )

        self.table = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=9
        )

        self.table.heading("sectionID", text="Section")
        self.table.heading("courseID", text="Course")
        self.table.heading("courseName", text="Course Name")
        self.table.heading("status", text="Status")
        self.table.heading("position", text="Position")

        self.table.column("sectionID", width=90, anchor="center")
        self.table.column("courseID", width=90, anchor="center")
        self.table.column("courseName", width=220)
        self.table.column("status", width=90, anchor="center")
        self.table.column("position", width=70, anchor="center")

        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_waitlist()

    # ==================================================
    # UC-S5 – VIEW WAITLIST STATUS
    # ==================================================
    def load_waitlist(self):
        self.table.delete(*self.table.get_children())

        # 🔥 CONTROLLER CALL
        waitlists = StudentController.view_waitlist_status(
            self.user["studentID"]
        )

        for w in waitlists:
            self.table.insert(
                "",
                "end",
                values=(
                    w["sectionID"],
                    w["courseID"],
                    w["courseName"],
                    w["status"],
                    w["position"]
                )
            )
