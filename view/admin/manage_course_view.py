import tkinter as tk
from tkinter import ttk, messagebox
from controller.admin_controller import AdminController


class ManageCourseView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.title("Manage Courses")
        self.geometry("1050x480")
        self.resizable(False, False)

        self.create_widgets()
        self.load_courses()

    def create_widgets(self):
        ttk.Label(
            self,
            text="Course Management",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        columns = (
            "courseID",
            "courseName",
            "credits",
            "prerequisite",
            "description"
        )

        self.course_table = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=12
        )

        self.course_table.heading("courseID", text="Course ID")
        self.course_table.heading("courseName", text="Course Name")
        self.course_table.heading("credits", text="Credits")
        self.course_table.heading("prerequisite", text="Prerequisites")
        self.course_table.heading("description", text="Description")

        self.course_table.column("courseID", width=120)
        self.course_table.column("courseName", width=230)
        self.course_table.column("credits", width=80, anchor="center")
        self.course_table.column("prerequisite", width=220)
        self.course_table.column("description", width=320)

        self.course_table.pack(
            fill=tk.BOTH, expand=True, padx=15, pady=10
        )

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Add New Course",
            width=18,
            command=self.open_add_course
        ).grid(row=0, column=0, padx=6)

        tk.Button(
            btn_frame,
            text="Edit Course",
            width=18,
            command=self.open_edit_course
        ).grid(row=0, column=1, padx=6)

        tk.Button(
            btn_frame,
            text="Add Prerequisite",
            width=18,
            command=self.open_add_prerequisite
        ).grid(row=0, column=2, padx=6)

        tk.Button(
            btn_frame,
            text="Edit Prerequisites",
            width=20,
            command=self.open_edit_prerequisite
        ).grid(row=0, column=3, padx=6)


    def load_courses(self):
        self.course_table.delete(*self.course_table.get_children())

        courses = AdminController.get_all_courses()

        for c in courses:
           
            prereq_text = ""
            if "prerequisites" in c and c["prerequisites"]:
                if isinstance(c["prerequisites"], list):
                    prereq_text = ", ".join(c["prerequisites"])
                else:
                    prereq_text = c["prerequisites"]

            self.course_table.insert(
                "",
                "end",
                values=(
                    c["courseID"],
                    c["courseName"],
                    c["credits"],
                    prereq_text,
                    c["description"]
                )
            )

   
    def get_selected_course_id(self):
        selected = self.course_table.selection()
        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a course first"
            )
            return None
        return self.course_table.item(selected[0])["values"][0]

    def open_add_course(self):
        from view.admin.manageCourView.add_course_view import AddCourseView
        AddCourseView(self)

    def open_edit_course(self):
        course_id = self.get_selected_course_id()
        if not course_id:
            return

        from view.admin.manageCourView.edit_course_view import EditCourseView
        EditCourseView(self, course_id)

    def open_add_prerequisite(self):
        course_id = self.get_selected_course_id()
        if not course_id:
            return

        from view.admin.manageCourView.add_prerequisite_view import AddPrerequisiteView
        AddPrerequisiteView(self, course_id)

    def open_edit_prerequisite(self):
        course_id = self.get_selected_course_id()
        if not course_id:
            return

        from view.admin.manageCourView.edit_prerequisite_view import EditPrerequisiteView
        EditPrerequisiteView(self, course_id)
