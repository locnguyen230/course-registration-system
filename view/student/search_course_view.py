import tkinter as tk
from controller.student_controller import StudentController

class SearchCourseView(tk.Frame):

    def __init__(self, dashboard, student_id):
        super().__init__(dashboard)
        self.dashboard = dashboard
        self.controller = StudentController()
        self.pack(fill="both", expand=True)

        tk.Label(self, text="SEARCH COURSE", font=("Arial", 16)).pack(pady=10)

        self.keyword_entry = tk.Entry(self, width=40)
        self.keyword_entry.pack()

        tk.Button(self, text="Search", command=self.search).pack(pady=5)

        self.listbox = tk.Listbox(self, width=80)
        self.listbox.pack()

        tk.Button(self, text="Back", command=self.dashboard.go_back).pack(pady=10)
