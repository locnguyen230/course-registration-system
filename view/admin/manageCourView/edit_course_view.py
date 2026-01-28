import tkinter as tk
from tkinter import ttk, messagebox
from controller.admin_controller import AdminController


class EditCourseView(tk.Toplevel):
    def __init__(self, parent, course_id):
        super().__init__(parent)

        self.parent = parent
        self.course_id = course_id

        self.title("Edit Course")
        self.geometry("420x330")
        self.resizable(False, False)

        self.create_widgets()
        self.load_course_info()

    # ===============================
    # UI
    # ===============================
    def create_widgets(self):
        ttk.Label(
            self,
            text="Edit Course",
            font=("Arial", 13, "bold")
        ).pack(pady=10)

        form = ttk.Frame(self)
        form.pack(padx=20, pady=10, fill=tk.X)

        # ===== Course ID (readonly) =====
        ttk.Label(form, text="Course ID:").grid(row=0, column=0, sticky="w", pady=6)
        self.course_id_entry = ttk.Entry(form, width=28, state="readonly")
        self.course_id_entry.grid(row=0, column=1, pady=6)

        # ===== Course Name =====
        ttk.Label(form, text="Course Name:").grid(row=1, column=0, sticky="w", pady=6)
        self.course_name_entry = ttk.Entry(form, width=28)
        self.course_name_entry.grid(row=1, column=1, pady=6)

        # ===== Credits =====
        ttk.Label(form, text="Credits:").grid(row=2, column=0, sticky="w", pady=6)
        self.credits_cb = ttk.Combobox(
            form,
            values=[0, 2, 3, 4],
            state="readonly",
            width=25
        )
        self.credits_cb.grid(row=2, column=1, pady=6)

        # ===== Description =====
        ttk.Label(form, text="Description:").grid(
            row=3, column=0, sticky="nw", pady=6
        )
        self.desc_text = tk.Text(form, width=30, height=5)
        self.desc_text.grid(row=3, column=1, pady=6)

        # ===== Buttons =====
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=15)

        ttk.Button(
            btn_frame,
            text="Save Changes",
            width=15,
            command=self.save_changes
        ).grid(row=0, column=0, padx=6)

        ttk.Button(
            btn_frame,
            text="Cancel",
            width=15,
            command=self.destroy
        ).grid(row=0, column=1, padx=6)

    # ===============================
    # LOAD DATA
    # ===============================
    def load_course_info(self):
        course = AdminController.get_course_by_id(self.course_id)

        if not course:
            messagebox.showerror("Error", "Course not found")
            self.destroy()
            return

        self.course_id_entry.config(state="normal")
        self.course_id_entry.insert(0, course["courseID"])
        self.course_id_entry.config(state="readonly")

        self.course_name_entry.insert(0, course["courseName"])
        self.credits_cb.set(course["credits"])
        self.desc_text.insert("1.0", course["description"])

    # ===============================
    # SAVE
    # ===============================
    def save_changes(self):
        course_name = self.course_name_entry.get().strip()
        credits = self.credits_cb.get()
        description = self.desc_text.get("1.0", tk.END).strip()

        if not course_name:
            messagebox.showwarning("Warning", "Course name is required")
            return

        success = AdminController.update_course(
            course_id=self.course_id,
            course_name=course_name,
            credits=credits,
            description=description
        )

        if success:
            messagebox.showinfo("Success", "Course updated successfully")
            self.parent.load_courses()
            self.destroy()
        else:
            messagebox.showerror("Error", "Update failed")
