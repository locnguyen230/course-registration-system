from model.dao.course_dao import CourseDAO
from model.dao.registration_dao import RegistrationDAO
from model.dao.waitlist_dao import WaitlistDAO
from model.dao.registration_batch_dao import RegistrationBatchDAO
from model.dao.student_dao import StudentDAO


class StudentController:

    def view_course_list():
        return CourseDAO.get_open_courses()
    
    def search_course(keyword):
        return CourseDAO.search_courses(keyword)

    def withdraw_course(student_id, section_id):
        return RegistrationDAO.withdraw(student_id, section_id)

    def join_waitlist(student_id, section_id):
        major = student_id[:2]  

        waitlist_id = WaitlistDAO.generate_waitlist_id(major)
        position = WaitlistDAO.get_next_position(section_id)

        WaitlistDAO.add_to_waitlist(
            waitlist_id,
            student_id,
            section_id,
            position
        )
       
    def view_waitlist_status(student_id):
        return WaitlistDAO.get_waitlist_status(student_id)
    
    def check_registrationbatch(student_id):
        batch = RegistrationBatchDAO.get_time(student_id)

        
        if not batch:
            return False, "⛔ Registration period is currently closed."
        
        start = batch["startTime"]
        end = batch["endTime"]
        batch_id = batch["batchID"]

        time_note = (
            f"🕒 Registration period: "
            f"{start.strftime('%d/%m/%Y %H:%M')} "
            f"→ {end.strftime('%d/%m/%Y %H:%M')}"
        )

        return True, time_note, batch_id
    
    def get_available_courses(student_id):
        result = CourseDAO.search_courses_registration(student_id[:2])
        return  result

    def register_course(student_id, section_id, batch_id, prereq):

        # 1. HANDLE PREREQUISITE
        if prereq and str(prereq).strip().lower() not in ("none", "null"):
            prereq_list = [
                p.strip()
                for p in prereq.split(",")
                if p.strip()
            ]
        else:
            prereq_list = []

        for course_id in prereq_list:
            if not RegistrationDAO.is_course_completed(student_id, course_id):
                return False, f"Missing prerequisite: {course_id}"

        # 2. REGISTER
        reg_id = RegistrationDAO.generate_registration_id(
            student_id[:2]
        )

        success = RegistrationDAO.register(
            reg_id,
            student_id,
            batch_id,
            section_id
        )

        if not success:
            return False, "Unable to register"

        return True, "Registration successful"
    
    def get_registrationrecord(student_id):
        return RegistrationDAO.get_course_regis_by_std(student_id)