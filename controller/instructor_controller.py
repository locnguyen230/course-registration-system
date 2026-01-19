import csv
import os
from model.dao.instructor_dao import InstructorDAO

class InstructorController:
    def __init__(self, current_user_id):
        self.dao = InstructorDAO()
        # Lấy profile giảng viên dựa trên account đang đăng nhập
        self.current_instructor = self.dao.get_instructor_by_user_id(current_user_id)

    def check_access(self):
        return self.current_instructor is not None

    def get_instructor_sections(self):
        """UC-I1: Lấy danh sách lớp"""
        if self.current_instructor:
            return self.dao.get_sections_by_instructor(self.current_instructor.instructor_id)
        return []

    def get_class_roster(self, section_id):
        """UC-I1: Lấy danh sách sinh viên"""
        return self.dao.get_students_in_section(section_id)

    def export_roster_to_csv(self, section_id, file_path="roster_export.csv"):
        """UC-I2: Xuất danh sách ra file CSV"""
        students = self.get_class_roster(section_id)
        if not students:
            return False, "No students to export."
        
        try:
            # Tạo thư mục nếu chưa tồn tại (để tránh lỗi path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True) if os.path.dirname(file_path) else None
            
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Header
                writer.writerow(['Student ID', 'Full Name', 'Email', 'Major', 'Year Level'])
                # Data
                for s in students:
                    writer.writerow([s.student_id, s.full_name, s.email, s.major, s.year_level])
            return True, f"Exported successfully to {file_path}"
        except Exception as e:
            return False, str(e)

    def get_override_requests(self):
        """UC-I3: Lấy danh sách yêu cầu"""
        if self.current_instructor:
            return self.dao.get_pending_waitlist_requests(self.current_instructor.instructor_id)
        return []

    def process_request(self, waitlist_id, decision):
        """UC-I3: Duyệt hoặc từ chối yêu cầu"""
        status_map = {
            'approve': 'APPROVED',
            'reject': 'REMOVED'
        }
        if decision not in status_map:
            return False
        
        return self.dao.update_waitlist_status(waitlist_id, status_map[decision])