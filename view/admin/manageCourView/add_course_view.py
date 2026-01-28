import tkinter as tk
from tkinter import ttk, messagebox
from controller.admin_controller import AdminController


class AddCourseView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.title("Add New Course")
        self.geometry("420x360")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(
            self,
            text="Add New Course",
            font=("Arial", 13, "bold")
        ).pack(pady=10)

        form = ttk.Frame(self)
        form.pack(padx=20, pady=10, fill=tk.X)


        ttk.Label(form, text="Major:").grid(row=0, column=0, sticky="w", pady=6)
        self.major_cb = ttk.Combobox(
            form,
            values=["IT", "LG", "CS", "SE"],
            state="readonly",
            width=25
        )
        self.major_cb.grid(row=0, column=1, pady=6)
        self.major_cb.current(0)

   
        ttk.Label(form, text="Course Name:").grid(row=1, column=0, sticky="w", pady=6)
        self.course_name_entry = ttk.Entry(form, width=28)
        self.course_name_entry.grid(row=1, column=1, pady=6)

        ttk.Label(form, text="Credits:").grid(row=2, column=0, sticky="w", pady=6)
        self.credits_cb = ttk.Combobox(
            form,
            values=[0, 2, 3, 4],
            state="readonly",
            width=25
        )
        self.credits_cb.grid(row=2, column=1, pady=6)
        self.credits_cb.current(1)

        ttk.Label(form, text="Description:").grid(
            row=3, column=0, sticky="nw", pady=6
        )
        self.desc_text = tk.Text(form, width=30, height=5)
        self.desc_text.grid(row=3, column=1, pady=6)


        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=15)

        ttk.Button(
            btn_frame,
            text="Save",
            width=14,
            command=self.save_course
        ).grid(row=0, column=0, padx=6)

        ttk.Button(
            btn_frame,
            text="Cancel",
            width=14,
            command=self.destroy
        ).grid(row=0, column=1, padx=6)

   
    def save_course(self):
        major = self.major_cb.get()
        course_name = self.course_name_entry.get().strip()
        credits = self.credits_cb.get()
        description = self.desc_text.get("1.0", tk.END).strip()

        if not course_name:
            messagebox.showwarning("Warning", "Course name is required")
            return

        success = AdminController.add_course(
            major=major,
            course_name=course_name,
            credits=credits,
            description=description
        )

        if success:
            messagebox.showinfo("Success", "Course added successfully")
            self.parent.load_courses()
            self.destroy()
        else:
            messagebox.showerror("Error", "Course added faild")
