import tkinter as tk
from tkinter import ttk, messagebox
from controller.admin_controller import AdminController


class CancelUnderEnrolledView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.title("Cancel Under-enrolled Classes")
        self.geometry("900x420")
        self.resizable(False, False)

        self.create_widgets()
        self.load_under_enrolled_sections()


    def create_widgets(self):
        ttk.Label(
            self,
            text="Under-enrolled Course Sections",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        columns = (
            "sectionID",
            "courseName",
            "enrollment",
            "instructorID"
        )

        self.section_table = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=12,
            selectmode="browse"  
        )

        self.section_table.heading("sectionID", text="Section ID")
        self.section_table.heading("courseName", text="Course Name")
        self.section_table.heading("enrollment", text="Enrolled / Capacity")
        self.section_table.heading("instructorID", text="Instructor ID")

        self.section_table.column("sectionID", width=120)
        self.section_table.column("courseName", width=320)
        self.section_table.column("enrollment", width=180, anchor="center")
        self.section_table.column("instructorID", width=160)

        self.section_table.pack(
            fill=tk.BOTH, expand=True, padx=15, pady=10
        )

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        ttk.Button(
            btn_frame,
            text="Cancel Class",
            width=25,
            command=self.cancel_selected_section
        ).grid(row=0, column=0, padx=8)

        ttk.Button(
            btn_frame,
            text="Close",
            width=15,
            command=self.destroy
        ).grid(row=0, column=1, padx=8)

    def load_under_enrolled_sections(self):
        self.section_table.delete(*self.section_table.get_children())

        sections = AdminController.get_info_classs()

        for s in sections:
            enrollment_text = f"{s['enrolledCount']} / {s['capacity']}"

            self.section_table.insert(
                "",
                "end",
                values=(
                    s["sectionID"],
                    s["courseName"],
                    enrollment_text,
                    s["instructorID"]
                )
            )

 
    def cancel_selected_section(self):
        selected = self.section_table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a class to cancel"
            )
            return

        section_id = self.section_table.item(selected[0])["values"][0]

        confirm = messagebox.askyesno(
            "Confirm Cancellation",
            f"Are you sure you want to cancel class {section_id}?"
        )

        if not confirm:
            return

        success = AdminController.cancel_section(section_id)

        if success:
            messagebox.showinfo(
                "Success",
                "Class has been cancelled"
            )
            self.load_under_enrolled_sections()
        else:
            messagebox.showerror(
                "Error",
                "Failed to cancel class"
            )
