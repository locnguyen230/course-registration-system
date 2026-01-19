class InstructorDashboard:
    def __init__(self, controller):
        self.controller = controller

    def display_menu(self):
        if not self.controller.check_access():
            print("Access Denied: You are not an instructor.")
            return

        instructor = self.controller.current_instructor
        while True:
            print(f"\n--- INSTRUCTOR DASHBOARD: {instructor.full_name} ---")
            print("1. View Class Roster (UC-I1)")
            print("2. Review Override Requests (UC-I3)")
            print("3. Exit")
            
            choice = input("Select an option: ")
            
            if choice == '1':
                from view.instructor.view_class_roster import ViewClassRoster
                ViewClassRoster(self.controller).show()
            elif choice == '2':
                from view.instructor.override_request_view import OverrideRequestView
                OverrideRequestView(self.controller).show()
            elif choice == '3':
                print("Goodbye.")
                break
            else:
                print("Invalid option.")