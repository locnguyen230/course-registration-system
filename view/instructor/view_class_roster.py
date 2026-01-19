from view.instructor.export_roster_view import ExportRosterView

class ViewClassRoster:
    def __init__(self, controller):
        self.controller = controller

    def show(self):
        # 1. Hiển thị danh sách lớp (UC-I1)
        sections = self.controller.get_instructor_sections()
        if not sections:
            print("No classes assigned to you.")
            return

        print("\n--- YOUR CLASSES ---")
        for idx, sec in enumerate(sections):
            print(f"{idx + 1}. {sec.section_code} - Enrolled: {sec.enrolled_count}/{sec.capacity}")
        
        # 2. Chọn lớp để xem chi tiết
        try:
            choice = int(input("Select a class to view roster (0 to cancel): "))
            if choice <= 0 or choice > len(sections):
                return
            
            selected_section = sections[choice - 1]
            self.display_roster(selected_section)
        except ValueError:
            print("Invalid input.")

    def display_roster(self, section):
        students = self.controller.get_class_roster(section.section_id)
        print(f"\n--- ROSTER FOR {section.section_code} ---")
        print(f"{'ID':<15} {'Name':<25} {'Email':<30}")
        print("-" * 70)
        for s in students:
            print(f"{s.student_id:<15} {s.full_name:<25} {s.email:<30}")
        
        # Gọi tính năng Export (UC-I2)
        ExportRosterView(self.controller).show_export_option(section.section_id)