import tkinter as tk
from tkinter import ttk, messagebox
# Import view export để gọi khi cần
from view.instructor.export_roster_view import ExportRosterView

class ViewClassRoster(tk.Frame):
    def __init__(self, parent, controller, switch_frame_callback):
        super().__init__(parent)
        self.controller = controller
        self.switch_frame = switch_frame_callback
        self.current_section_id = None
        
        # Layout
        top_bar = tk.Frame(self)
        top_bar.pack(fill=tk.X, padx=10, pady=10)
        
        # Nút quay lại
        tk.Button(top_bar, text="< Quay lại", command=lambda: self.switch_frame("dashboard")).pack(side=tk.LEFT)
        tk.Label(top_bar, text="QUẢN LÝ DANH SÁCH LỚP HỌC", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=20)
        
        # Dropdown chọn lớp học
        select_frame = tk.Frame(self)
        select_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(select_frame, text="Chọn lớp học:").pack(side=tk.LEFT)
        
        # Lấy danh sách lớp từ controller
        self.sections = self.controller.get_instructor_sections()
        section_values = [f"{s.section_code} - {s.semester}" for s in self.sections]
        
        self.cb_sections = ttk.Combobox(select_frame, values=section_values, state="readonly", width=40)
        self.cb_sections.pack(side=tk.LEFT, padx=10)
        self.cb_sections.bind("<<ComboboxSelected>>", self.on_section_select)
        
        # Nút Export (UC-I2)
        self.btn_export = tk.Button(select_frame, text="Xuất Danh Sách (Export)", bg="#4CAF50", fg="white", 
                                    state=tk.DISABLED, command=self.open_export_view)
        self.btn_export.pack(side=tk.RIGHT)

        # Bảng hiển thị sinh viên (Treeview)
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ("id", "name", "email", "major", "year")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        self.tree.heading("id", text="MSSV")
        self.tree.heading("name", text="Họ tên")
        self.tree.heading("email", text="Email")
        self.tree.heading("major", text="Ngành")
        self.tree.heading("year", text="Năm thứ")
        
        self.tree.column("id", width=100)
        self.tree.column("name", width=200)
        self.tree.column("email", width=250)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def on_section_select(self, event):
        idx = self.cb_sections.current()
        if idx >= 0:
            section = self.sections[idx]
            self.current_section_id = section.section_id
            self.load_data(section.section_id)
            self.btn_export.config(state=tk.NORMAL)

    def load_data(self, section_id):
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Lấy dữ liệu mới từ controller
        students = self.controller.get_class_roster(section_id)
        for s in students:
            self.tree.insert("", tk.END, values=(s.student_id, s.full_name, s.email, s.major, s.year_level))

    def open_export_view(self):
        # Gọi file view export (Popup)
        if self.current_section_id:
            ExportRosterView(self, self.controller, self.current_section_id)