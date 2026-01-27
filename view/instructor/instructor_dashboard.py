import tkinter as tk
from tkinter import ttk, messagebox
from controller.instructor_controller import InstructorController


class InstructorDashboard(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.user = user  

        self.title("Instructor Dashboard")
        self.geometry("1500x450")

        tk.Label(
            self,
            text=f"Welcome Instructor: {user.get('fullName', '')}",
            font=("Arial", 14)
        ).pack(pady=5)

        # ===============================
        # UC-I1 – VIEW CLASS ROSTER (DEFAULT)
        # ===============================
        columns = (
            "sectionID",
            "courseID",
            "courseName",
            "sectionCode",
            "semester",
            "enrolled"
        )

        self.class_table = ttk.Treeview(
            self, columns=columns, show="headings", height=10
        )

        self.class_table.heading("sectionID", text="Section ID")
        self.class_table.heading("courseID", text="Course")
        self.class_table.heading("courseName", text="Course Name")
        self.class_table.heading("sectionCode", text="Section Code")
        self.class_table.heading("semester", text="Semester")
        self.class_table.heading("enrolled", text="Enrolled")

        self.class_table.pack(fill="both", expand=True, padx=10, pady=5)

        self.load_class_list()

        # ===============================
        # ACTION BUTTONS
        # ===============================
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Show Student List",
            command=self.show_students
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Export Roster",
            command=self.export_roster
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame,
            text="Review Override Requests",
            command=self.open_override_requests
        ).grid(row=0, column=2, padx=5)

    # ==================================================
    # UC-I1 – VIEW CLASS LIST (DEFAULT LOAD)
    # ==================================================
    def load_class_list(self):
        self.class_table.delete(*self.class_table.get_children())

        # 🔥 CONTROLLER CALL
        classes = InstructorController.view_class_list(
            self.user["instructorID"]
        )

        for c in classes:
            self.class_table.insert(
                "",
                "end",
                values=(
                    c["sectionID"],
                    c["courseID"],
                    c["courseName"],
                    c["sectionCode"],
                    c["semester"],
                    f'{c["enrolledCount"]}/{c["capacity"]}'
                )
            )

    # ==================================================
    # UC-I1 – SHOW STUDENT LIST
    # ==================================================
    def show_students(self):
        selected = self.class_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a class")
            return

        section_id = self.class_table.item(selected[0])["values"][0]

        from view.instructor.view_class_roster import StudentRosterView
        StudentRosterView(self, section_id)

    # ==================================================
    # UC-I2 – EXPORT STUDENT ROSTER
    # ==================================================
    def export_roster(self):
        selected = self.class_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a class")
            return

        section_id = self.class_table.item(selected[0])["values"][0]


        success, path = InstructorController.export_roster(section_id)
       
        if success:
            messagebox.showinfo("Success", path)
        else:
            messagebox.showerror("Error", "Can not export!")

    # ==================================================
    # UC-I3 – REVIEW OVERRIDE REQUESTS
    # ==================================================
    def open_override_requests(self):
        from view.instructor.override_request_view import OverrideRequestView
        OverrideRequestView(self, self.user["instructorID"])


