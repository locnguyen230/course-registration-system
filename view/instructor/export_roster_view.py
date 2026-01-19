import tkinter as tk
from tkinter import filedialog, messagebox

class ExportRosterView:
    def __init__(self, parent_view, controller, section_id):
        self.controller = controller
        self.section_id = section_id
        self.parent = parent_view
        
        # Thực hiện logic export ngay khi gọi
        self.show_export_dialog()

    def show_export_dialog(self):
        # Mở hộp thoại chọn nơi lưu file của hệ thống
        file_path = filedialog.asksaveasfilename(
            parent=self.parent,
            defaultextension=".csv",
            initialfile=f"roster_{self.section_id}",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Lưu danh sách sinh viên"
        )
        
        if file_path:
            success, message = self.controller.export_roster_to_csv(self.section_id, file_path)
            if success:
                messagebox.showinfo("Thành công", message)
            else:
                messagebox.showerror("Lỗi", message)