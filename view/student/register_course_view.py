import tkinter as tk
from tkinter import ttk, messagebox

from controller.student_controller import StudentController


class RegisterCourseWindow(tk.Toplevel):
    def __init__(self, parent, user, context_text, batch_id):
        super().__init__(parent)
        self.user = user
        self.batch_id = batch_id
        self.title("Register Course")
        self.geometry("760x400")

        # ===============================
        # REGISTRATION BATCH INFO
        # ===============================
        tk.Label(
            self,
            text=context_text,
            fg="green",
            font=("Arial", 10, "italic")
        ).pack(pady=5)

        tk.Label(
            self,
            text="Available Courses for Registration",
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        # ===============================
        # TABLE
        # ===============================
        columns = (
            "sectionID",
            "courseName",
            "prerequisites",
            "available"
        )

        self.table = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=9
        )

        self.table.heading("sectionID", text="section ID")
        self.table.heading("courseName", text="Course Name")
        self.table.heading("prerequisites", text="Prerequisites")
        self.table.heading("available", text="Available")

        self.table.column("sectionID", width=100, anchor="center")
        self.table.column("courseName", width=220)
        self.table.column("prerequisites", width=260)
        self.table.column("available", width=80, anchor="center")

        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        # ===============================
        # BUTTON
        # ===============================
        tk.Button(
            self,
            text="Register",
            width=18,
            command=self.handle_register
        ).pack(pady=8)

        self.load_courses()

    # ==================================================
    # LOAD AVAILABLE COURSES
    # ==================================================
    def load_courses(self):
        self.table.delete(*self.table.get_children())

        # 🔥 DEMO DATA
        # SAU NÀY THAY BẰNG:
        courses = StudentController.get_available_courses(self.user["studentID"])


        for c in courses:

            available_display = (
                c["available"] if int(c["available"]) > 0 else "FULL"
            )

            self.table.insert(
                "",
                "end",
                values=(
                    c["sectionID"],
                    c["courseName"],
                    c["prerequisites"],
                    available_display
                )
            )

    # ==================================================
    # UC-S3 – REGISTER COURSE
    # ==================================================
    def handle_register(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a course"
            )
            return

        item = self.table.item(selected[0])
        section_id, course_name, prereq, available = item["values"]

        # ===============================
        # CASE 1: COURSE FULL → WAITLIST
        # ===============================
        if str(available).upper() == "FULL":
            join = messagebox.askyesno(
                "Course Full",
                f"{section_id} is full.\nDo you want to join the waitlist?"
            )

            if join:
                # 🔥 CONTROLLER CALL
                StudentController.join_waitlist(
                    self.user["studentID"],
                    section_id
                )

                messagebox.showinfo(
                    "Waitlist",
                    f"You have joined the waitlist for {section_id}"
                )
            return

        # ===============================
        # CASE 2: AVAILABLE → REGISTER
        # ===============================
        # 🔥 CONTROLLER CALL
        success, msg = StudentController.register_course(
            self.user["studentID"],
            section_id,
            self.batch_id,
            prereq
        )
        if not success:
            messagebox.showerror("Register failed", msg)
        else:
            messagebox.showinfo("Success", msg)

