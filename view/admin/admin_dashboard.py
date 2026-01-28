import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from controller.admin_controller import AdminController


class AdminDashboard(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.user = user

        self.title("Admin Dashboard")
        self.geometry("1400x600")

        tk.Label(
            self,
            text=f"Welcome Admin: {user.get('fullName', '')}",
            font=("Arial", 14)
        ).pack(pady=5)

        # ===============================
        # DEMO OVERVIEW DATA (UC-A10)
        # ===============================
        overview_stats = AdminController.get_overview()
        # ===============================
        # OVERVIEW CHART (TOP)
        # ===============================
        chart_frame = tk.Frame(self)
        chart_frame.pack(fill=tk.BOTH, expand=True)

        self.draw_overview_chart(chart_frame, overview_stats)

        # ===============================
        # ACTION BUTTONS (BOTTOM)
        # ===============================
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Manage Students", width=22,
                  command=self.open_manage_students).grid(row=0, column=0, padx=6)

        tk.Button(btn_frame, text="Manage Courses", width=22,
                  command=self.open_manage_courses).grid(row=0, column=1, padx=6)

        tk.Button(btn_frame, text="Registration Batches", width=22,
                  command=self.open_batches).grid(row=0, column=2, padx=6)

        tk.Button(btn_frame, text="Academic Config", width=22,
                  command=self.open_academic).grid(row=0, column=3, padx=6)

        tk.Button(btn_frame, text="Cancel Classes", width=22,
                  command=self.open_cancel_class).grid(row=0, column=4, padx=6)
        tk.Button(
            btn_frame,
            text="Bulk Import Data",
            width=22,
            command=self.bulk_import
        ).grid(row=1, column=1, padx=6, pady=8)

        tk.Button(
            btn_frame,
            text="Bulk Export Data",
            width=22,
            command=self.bulk_export
        ).grid(row=1, column=2, padx=6, pady=8)

    # ===============================
    # BAR CHART – SYSTEM OVERVIEW
    # ===============================
    def draw_overview_chart(self, parent, data):
        fig = Figure(figsize=(10, 4))
        ax = fig.add_subplot(111)

        ax.bar(data.keys(), data.values())
        ax.set_title("System Overview Statistics")
        ax.set_ylabel("Count")

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

    # ===============================
    # OPEN UC WINDOWS
    # ===============================
    def open_manage_students(self):
        from view.admin.manage_student_view import ManageStudentView
        ManageStudentView(self)

        
    def open_manage_courses(self):
        from view.admin.manage_course_view import ManageCourseView
        ManageCourseView(self)


    def open_batches(self):
        from view.admin.manage_registration_batch_view import ManageRegistrationBatchView
        ManageRegistrationBatchView(self)


    def open_academic(self):
        from view.admin.academic_config_view import AcademicConfigView
        AcademicConfigView(self)

    def open_cancel_class(self):
        from view.admin.cancel_under_enrolled_view import CancelUnderEnrolledView
        CancelUnderEnrolledView(self)

    def bulk_import(self):
        from view.admin.bulk_import_view import ImportAcademicConfigView
        ImportAcademicConfigView(self)


    def bulk_export(self):
        success, file_path = AdminController.export_overview_stats()
        if success:
            messagebox.showinfo("Success", file_path)
        else:
            messagebox.showerror("Error","Export faild")