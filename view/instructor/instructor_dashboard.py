import tkinter as tk
from tkinter import ttk

class InstructorDashboard(tk.Frame):
    def __init__(self, parent, controller, switch_frame_callback):
        super().__init__(parent)
        self.controller = controller
        self.switch_frame = switch_frame_callback
        
        # Lấy thông tin giảng viên
        instructor = self.controller.current_instructor
        
        # Giao diện
        self.configure(bg="white")
        
        # Header
        lbl_title = tk.Label(self, text=f"DASHBOARD GIẢNG VIÊN", font=("Arial", 20, "bold"), bg="white", fg="#1976D2")
        lbl_title.pack(pady=(30, 10))
        
        lbl_name = tk.Label(self, text=f"Xin chào: {instructor.full_name} ({instructor.department})", font=("Arial", 12), bg="white")
        lbl_name.pack(pady=(0, 30))
        
        # Frame chứa các nút chức năng
        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack()
        
        # Nút UC-I1: Xem danh sách lớp
        btn_roster = tk.Button(btn_frame, text="Xem Danh Sách Lớp (Class Roster)", 
                               font=("Arial", 12), bg="#2196F3", fg="white", width=30, height=2,
                               command=lambda: self.switch_frame("view_roster"))
        btn_roster.grid(row=0, column=0, pady=10)

        # Nút UC-I3: Duyệt yêu cầu
        btn_override = tk.Button(btn_frame, text="Duyệt Yêu Cầu (Override Requests)", 
                                 font=("Arial", 12), bg="#FF9800", fg="white", width=30, height=2,
                                 command=lambda: self.switch_frame("view_override"))
        btn_override.grid(row=1, column=0, pady=10)
        
        # Nút Đăng xuất
        btn_logout = tk.Button(btn_frame, text="Đăng xuất", 
                               font=("Arial", 12), bg="#757575", fg="white", width=30,
                               command=lambda: self.switch_frame("login"))
        btn_logout.grid(row=2, column=0, pady=10)