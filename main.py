from controller.auth_controller import AuthController
from controller.instructor_controller import InstructorController
from view.instructor.instructor_dashboard import InstructorDashboard

def main():
    print("--- COURSE REGISTRATION SYSTEM ---")
    
    # [cite_start]1. Màn hình Đăng nhập (UC1) [cite: 161]
    auth = AuthController()
    username = input("Username: ")
    password = input("Password: ")
    
    is_success, user_obj, message = auth.login(username, password)
    
    if is_success:
        print(f"\n{message}")
        # Nếu là Instructor, khởi tạo controller của Instructor và chuyển sang Dashboard
        # user_obj ở đây là đối tượng Instructor trả về từ AuthController
        
        # Khởi tạo InstructorController với user_id của giảng viên này
        instructor_ctrl = InstructorController(user_obj.user_id)
        
        # [cite_start]Hiển thị Dashboard (UC-I1 start point) [cite: 170]
        dashboard = InstructorDashboard(instructor_ctrl)
        dashboard.display_menu()
        
    else:
        print(f"\nLỗi: {message}")

if __name__ == "__main__":
    main()