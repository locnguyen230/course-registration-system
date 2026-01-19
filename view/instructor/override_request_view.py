import tkinter as tk
from tkinter import ttk, messagebox

class OverrideRequestView(tk.Frame):
    def __init__(self, parent, controller, switch_frame_callback):
        super().__init__(parent)
        self.controller = controller
        self.switch_frame = switch_frame_callback
        
        # Header
        top_bar = tk.Frame(self)
        top_bar.pack(fill=tk.X, padx=10, pady=10)
        tk.Button(top_bar, text="< Quay lại", command=lambda: self.switch_frame("dashboard")).pack(side=tk.LEFT)
        tk.Label(top_bar, text="XỬ LÝ YÊU CẦU ĐĂNG KÝ (OVERRIDE)", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=20)
        
        # Bảng danh sách yêu cầu
        list_frame = tk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ("wid", "student_id", "name", "class", "date")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        self.tree.heading("wid", text="ID")
        self.tree.heading("student_id", text="MSSV")
        self.tree.heading("name", text="Tên Sinh Viên")
        self.tree.heading("class", text="Lớp Học phần")
        self.tree.heading("date", text="Ngày gửi")
        
        self.tree.column("wid", width=50)
        self.tree.column("name", width=200)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Load dữ liệu ban đầu
        self.load_requests()
        
        # Panel điều khiển (Nút bấm)
        btn_frame = tk.Frame(self, bg="#eee", height=50)
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        tk.Button(btn_frame, text="CHẤP THUẬN (Approve)", bg="green", fg="white", font=("Arial", 10, "bold"),
                  command=self.approve_request).pack(side=tk.RIGHT, padx=20, pady=10)
                  
        tk.Button(btn_frame, text="TỪ CHỐI (Reject)", bg="red", fg="white", font=("Arial", 10, "bold"),
                  command=self.reject_request).pack(side=tk.RIGHT, padx=10, pady=10)

    def load_requests(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        requests = self.controller.get_override_requests()
        for r in requests:
            self.tree.insert("", tk.END, values=(
                r['waitlistID'], r['studentID'], r['fullName'], r['sectionCode'], r['requestDate']
            ))

    def get_selected_id(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một yêu cầu để xử lý.")
            return None
        item = self.tree.item(selected[0])
        return item['values'][0] # Trả về waitlistID

    def approve_request(self):
        wid = self.get_selected_id()
        if wid:
            if self.controller.process_request(str(wid), 'approve'):
                messagebox.showinfo("Thông báo", "Đã CHẤP THUẬN yêu cầu.")
                self.load_requests() # Refresh lại bảng
            else:
                messagebox.showerror("Lỗi", "Có lỗi xảy ra khi xử lý.")

    def reject_request(self):
        wid = self.get_selected_id()
        if wid:
            confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn từ chối yêu cầu này?")
            if confirm:
                if self.controller.process_request(str(wid), 'reject'):
                    messagebox.showinfo("Thông báo", "Đã TỪ CHỐI yêu cầu.")
                    self.load_requests()
                else:
                    messagebox.showerror("Lỗi", "Có lỗi xảy ra khi xử lý.")