import tkinter as tk
from controller.auth_controller import AuthController
from controller.instructor_controller import InstructorController

# Import các file view vừa tạo
from view.instructor.instructor_dashboard import InstructorDashboard
from view.instructor.view_class_roster import ViewClassRoster
from view.instructor.override_request_view import OverrideRequestView

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hệ thống Đăng ký học phần")
        self.geometry("900x600")
        
        # Container chính chứa các View
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        # Biến lưu controller
        self.auth_ctrl = AuthController()
        self.instructor_ctrl = None
        
        # Bắt đầu bằng màn hình login (vẽ đơn giản tại đây hoặc tách file riêng)
        self.show_login_frame()

    def show_login_frame(self):
        self.clear_container()
        
        # Login Frame đơn giản
        frame = tk.Frame(self.container)
        frame.pack(expand=True)
        
        tk.Label(frame, text="ĐĂNG NHẬP", font=("Arial", 16)).pack(pady=10)
        
        tk.Label(frame, text="Username:").pack()
        entry_user = tk.Entry(frame)
        entry_user.pack()
        
        tk.Label(frame, text="Password:").pack()
        entry_pass = tk.Entry(frame, show="*")
        entry_pass.pack()
        
        def handle_login():
            user = entry_user.get()
            pwd = entry_pass.get()
            success, user_obj, msg = self.auth_ctrl.login(user, pwd)
            if success:
                # Khởi tạo Instructor Controller
                self.instructor_ctrl = InstructorController(user_obj.user_id)
                self.switch_frame("dashboard")
            else:
                tk.messagebox.showerror("Lỗi", msg)
                
        tk.Button(frame, text="Login", command=handle_login).pack(pady=20)

    def switch_frame(self, frame_name):
        self.clear_container()
        
        if frame_name == "dashboard":
            view = InstructorDashboard(self.container, self.instructor_ctrl, self.switch_frame)
        elif frame_name == "view_roster":
            view = ViewClassRoster(self.container, self.instructor_ctrl, self.switch_frame)
        elif frame_name == "view_override":
            view = OverrideRequestView(self.container, self.instructor_ctrl, self.switch_frame)
        elif frame_name == "login":
            self.show_login_frame()
            return

        view.pack(fill="both", expand=True)

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()