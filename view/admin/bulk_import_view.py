import tkinter as tk
from tkinter import ttk, messagebox
from controller.admin_controller import AdminController


class ImportAcademicConfigView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Import Academic Configuration")
        self.geometry("520x500")
        self.resizable(False, False)

        self.create_widgets()


    def create_widgets(self):
        ttk.Label(
            self,
            text="Import Academic Configuration",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

 
        instruction = (
            "Please enter the full file path to the CSV file.\n"
            "Example file path:\n"
            "C:/Users/Admin/Documents/academic_config.csv\n\n"
            "Please provide a CSV file with the following columns:\n\n"
            "academicYear, semester, policies\n\n"
            "Example:\n"
            "2025-2026, HK1, MaxCredits=24\n"
            "2025-2026, HK2, MaxCredits=24"
        )

        ttk.Label(
            self,
            text=instruction,
            wraplength=480,
            justify="left"
        ).pack(padx=15, pady=10)

  
        form = ttk.Frame(self)
        form.pack(padx=20, pady=10, fill=tk.X)

        ttk.Label(form, text="File path").grid(row=0, column=0, sticky="w", pady=5)
        self.file_entry = ttk.Entry(form, width=45)
        self.file_entry.grid(row=0, column=1, pady=5)

    
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=15)

        ttk.Button(
            btn_frame,
            text="Import",
            width=15,
            command=self.import_file
        ).grid(row=0, column=0, padx=8)

        ttk.Button(
            btn_frame,
            text="Cancel",
            width=15,
            command=self.destroy
        ).grid(row=0, column=1, padx=8)

    def import_file(self):
        file_path = self.file_entry.get().strip()

        if not file_path:
            messagebox.showerror(
                "Error",
                "Please enter a valid file path"
            )
            return

        success, msg = AdminController.import_academic_config(file_path)

        if success:
            messagebox.showinfo("Import Result", msg)
            self.destroy()
        else:
            messagebox.showerror("Import Failed", msg)
