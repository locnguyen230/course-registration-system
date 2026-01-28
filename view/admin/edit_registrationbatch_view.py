import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controller.admin_controller import AdminController


class EditRegistrationBatchView(tk.Toplevel):
    def __init__(self, parent, batch_id):
        super().__init__(parent)

        self.batch_id = batch_id

        self.title("Edit Registration Batch")
        self.geometry("420x350")
        self.resizable(False, False)

        # call controller
        batch = AdminController.get_batch_by_id(batch_id)
        

        form = tk.Frame(self)
        form.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Semester
        tk.Label(form, text="Semester").grid(row=0, column=0, sticky="w", pady=5)
        self.semester_entry = tk.Entry(form, width=25)
        self.semester_entry.insert(0, batch["semester"])
        self.semester_entry.grid(row=0, column=1, pady=5)

        # Start Time
        tk.Label(form, text="Start Date (yyyy/mm/dd)").grid(row=1, column=0, sticky="w", pady=5)
        self.start_entry = tk.Entry(form, width=25)
        self.start_entry.insert(0, batch["startTime"])
        self.start_entry.grid(row=1, column=1, pady=5)

        # End Time
        tk.Label(form, text="End Date (yyyy/mm/dd)").grid(row=2, column=0, sticky="w", pady=5)
        self.end_entry = tk.Entry(form, width=25)
        self.end_entry.insert(0, batch["endTime"])
        self.end_entry.grid(row=2, column=1, pady=5)

        # Eligible Year Level
        tk.Label(form, text="Eligible Year Level").grid(row=3, column=0, sticky="w", pady=5)
        self.year_combo = ttk.Combobox(
            form,
            values=["1", "2", "3", "4"],
            state="readonly",
            width=22
        )
        self.year_combo.set(batch["eligibleYearLevel"])
        self.year_combo.grid(row=3, column=1, pady=5)

      
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame, text="Update", width=12,
            command=self.update_batch
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame, text="Cancel", width=12,
            command=self.destroy
        ).grid(row=0, column=1, padx=5)

  
    def update_batch(self):
        semester = self.semester_entry.get().strip()
        start_date = self.start_entry.get().strip()
        end_date = self.end_entry.get().strip()
        eligible_year = self.year_combo.get()

        if not semester or not start_date or not end_date:
            messagebox.showwarning(
                "Validation Error",
                "Please fill all required fields"
            )
            return

        try:
            start_dt = datetime.strptime(start_date, "%Y/%m/%d")
            end_dt = datetime.strptime(end_date, "%Y/%m/%d")
        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Date format must be yyyy/mm/dd"
            )
            return

        if start_dt >= end_dt:
            messagebox.showerror(
                "Invalid Time",
                "Start date must be before end date"
            )
            return

        # call controller
        success = AdminController.update_registration_batch(
            self.batch_id,
            semester,
            start_dt,
            end_dt,
            eligible_year
        )

        if success:
            messagebox.showinfo(
            "Success",
            f"Registration batch '{self.batch_id}' updated successfully"
            )
        else:
            messagebox.showerror("Error",f"Registration batch '{self.batch_id}' updated faild")

        self.destroy()
