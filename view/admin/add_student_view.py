import tkinter as tk
from tkinter import ttk, messagebox
from controller.admin_controller import AdminController


class AddStudentView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Add New Student")
        self.geometry("420x420")
        self.resizable(False, False)

        # ===============================
        # FORM FRAME
        # ===============================
        form = tk.Frame(self, padx=20, pady=15)
        form.pack(fill="both", expand=True)

        # -------- USER INFO ----------
        tk.Label(form, text="Username").grid(row=0, column=0, sticky="w")
        self.username_entry = tk.Entry(form, width=30)
        self.username_entry.grid(row=0, column=1, pady=5)

        tk.Label(form, text="Password").grid(row=1, column=0, sticky="w")
        self.password_entry = tk.Entry(form, width=30, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        # -------- STUDENT INFO ----------
        tk.Label(form, text="Full Name").grid(row=2, column=0, sticky="w")
        self.fullname_entry = tk.Entry(form, width=30)
        self.fullname_entry.grid(row=2, column=1, pady=5)

        tk.Label(form, text="Email").grid(row=3, column=0, sticky="w")
        self.email_entry = tk.Entry(form, width=30)
        self.email_entry.grid(row=3, column=1, pady=5)

        tk.Label(form, text="Major").grid(row=4, column=0, sticky="w")
        self.major_cb = ttk.Combobox(
            form,
            values=["IT", "LG", "SE", "AI"],
            state="readonly",
            width=27
        )
        self.major_cb.grid(row=4, column=1, pady=5)
        self.major_cb.current(0)

        tk.Label(form, text="Year Level").grid(row=5, column=0, sticky="w")
        self.year_cb = ttk.Combobox(
            form,
            values=[1, 2, 3, 4],
            state="readonly",
            width=27
        )
        self.year_cb.grid(row=5, column=1, pady=5)
        self.year_cb.current(0)

        # ===============================
        # BUTTONS
        # ===============================
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame,
            text="Add Student",
            width=15,
            command=self.add_student
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Cancel",
            width=15,
            command=self.destroy
        ).grid(row=0, column=1, padx=5)

    # ===============================
    # ACTION
    # ===============================
    def add_student(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        full_name = self.fullname_entry.get().strip()
        email = self.email_entry.get().strip()
        major = self.major_cb.get()
        year_level = self.year_cb.get()

        if not all([username, password, full_name, email]):
            messagebox.showwarning("Warning", "Please fill all required fields")
            return

        success = AdminController.add_student(
            username=username,
            password=password,
            full_name=full_name,
            email=email,
            major=major,
            year_level=year_level
        )

        if success:
            messagebox.showinfo("Success", "Student added successfully")
            self.destroy()
        else:
            messagebox.showerror("Error", "Failed to add student")
