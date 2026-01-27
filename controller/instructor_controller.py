import csv
from pathlib import Path
from controller.student_controller import StudentController
from model.dao.instructor_dao import InstructorDAO
from model.dao.registration_batch_dao import RegistrationBatchDAO

class InstructorController:
    def view_class_list(instructor_id):
        return InstructorDAO.view_class_list(instructor_id)
    
    def get_students_by_section(section_id):
        return InstructorDAO.view_student_in_section(section_id)
    
    def export_roster(section_id):
        students = InstructorDAO.view_student_in_section(section_id)

        if not students:
            return None

        file_path = Path(f"roster_{section_id}.csv")

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Student ID", "Full Name", "Email"])

            for s in students:
                writer.writerow([
                    s["studentID"],
                    s["fullName"],
                    s["email"]
                ])

        return True, file_path
    
    def get_override_requests(instructor_id):
        return InstructorDAO.get_requests(instructor_id)
    
    def process_override(waitlist_id, status):

        wl = InstructorDAO.get_waitlist(waitlist_id)

        if wl is None:
            return False, "Waitlist request not found"

        if wl["status"] != "WAITING":
            return False, "Request already processed"

        # ===============================
        # REJECT
        # ===============================
        if status == "REMOVED":
            InstructorDAO.update_waitlist_status(
                waitlist_id, "REMOVED"
            )
            
            InstructorDAO.update_waitlist_position(
                wl["sectionID"], wl["position"]
            )

            return True, "Request rejected"
        
        # ===============================
        # APPROVE (OVERRIDE)
        # ===============================
        if status == "APPROVED":

            batch_id = RegistrationBatchDAO.get_batch_id( wl["studentID"])

            InstructorDAO.increase_capacity(wl["sectionID"])

            success, msg = StudentController.register_course(
                student_id=wl["studentID"],
                section_id=wl["sectionID"],
                batch_id = batch_id,
                prereq=wl["prerequisite"]   
            )

            if not success:
                return False, msg

            InstructorDAO.update_waitlist_status(
                waitlist_id, "APPROVED"
            )

            

            InstructorDAO.update_waitlist_position(
                wl["sectionID"], wl["position"]
            )


            return True, "Student approved and registered"

        return False, "Invalid status"
