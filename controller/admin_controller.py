import uuid
import bcrypt
import csv
from pathlib import Path
from datetime import datetime, time
from model.dao.admin_dao import AdminDAO
from model.dao.registration_batch_dao import RegistrationBatchDAO
from model.dao.course_dao import CourseDAO

class AdminController:
    def get_overview():
        return AdminDAO.get_dashboard_statistics()
    
    def get_info_edit(student_id):
        return AdminDAO.get_info_student(student_id)
    
    def get_list_student():
        return AdminDAO.get_all_student()
    
    def update_student(student_id,userName ,fullName ,email, password,academic_status):
        newpass = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user_id = AdminDAO.get_user_id_by_student_id(student_id)

        check1 = AdminDAO.update_student_info(user_id, fullName, email, academic_status)
        check2 = AdminDAO.update_user_info(user_id, userName,newpass)
        return check1 and check2
    
    def add_student(username, password, full_name, email, major, year_level):
   
        hashed_password = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()

       
        user_id = str(uuid.uuid4())

       
        next_number = AdminDAO.get_next_student_number_by_major(major)
        student_id = f"{major.upper()}{next_number:010d}"


        check_user = AdminDAO.add_new_user(
            user_id=user_id,
            username=username,
            password=hashed_password,
            role="STUDENT",
            status="ACTIVE"
        )

        if not check_user:
            return False

        check_student = AdminDAO.add_new_student(
            student_id=student_id,
            full_name=full_name,
            email=email,
            major=major.upper(),
            year_level=year_level,
            academic_status="ENROLLED",
            user_id=user_id
        )

        return check_student
    
    def delete_student(student_id):
        user_id =  AdminDAO.get_user_id_by_student_id(student_id)
        return AdminDAO.delete_student_by_userid(user_id, status="LOCKED")
     
    def get_registration_batches():
        return RegistrationBatchDAO.get_all()
    
    def get_batch_by_id(batch_id):
        batch = RegistrationBatchDAO.get_by_batchid(batch_id)
        if batch:
            batch["startTime"] = batch["startTime"].strftime("%Y/%m/%d")
            batch["endTime"] = batch["endTime"].strftime("%Y/%m/%d")
        return batch
    
    def update_registration_batch(batch_id, semester, start_dt,end_dt,eligible_year):
        new_start_dt = datetime.combine(start_dt, time(0, 0, 0))
        new_end_dt = datetime.combine(end_dt, time(23, 59, 59))
        return RegistrationBatchDAO.update_batch(batch_id, semester, new_start_dt, new_end_dt,eligible_year)
    
    def add_registration_batch(semester, start_dt,end_dt,eligible_year):
        new_start_dt = datetime.combine(start_dt, time(0, 0, 0))
        new_end_dt = datetime.combine(end_dt, time(23, 59, 59))
        batch_id = RegistrationBatchDAO.get_next_batch_id()
        return RegistrationBatchDAO.insert_batch(batch_id, semester, new_start_dt, new_end_dt,eligible_year)
    
    def get_academic_configs():
        return AdminDAO.get_info_config()
    
    def create_academic_config(academic_year, semester, policies):
        year = academic_year[:4]
        config_id = f"CFG-{semester}-{year}"
        return AdminDAO.add_new_config(config_id,academic_year,semester,policies)
    
    def update_config_by_id(config_id,academic_year,semester,policies):
        return AdminDAO.update_config(config_id,academic_year,semester,policies)
    
    def get_academic_config_by_id(config_id):
        return AdminDAO.get_config_by_id(config_id)
    
    def get_info_classs():
        return AdminDAO.get_class()
    
    def cancel_section(section_id):
        return AdminDAO.cancel_class(section_id, status = "CANCELED")
    
    def get_all_courses():
        return CourseDAO.get_courses()
    
    def add_course(major, course_name, credits, description):
        max_num = CourseDAO.get_max_course_number_by_major(major)

        next_num = 1 if max_num is None else max_num + 1

        course_id = f"{major}{next_num:04d}"

        return CourseDAO.add_course(
            course_id,
            course_name,
            credits,
            description
        )
    def get_course_by_id(course_id):
        return CourseDAO.get_course(course_id)
    
    def update_course(course_id,course_name,credits,description):
        return CourseDAO.update_course(course_id,course_name,credits,description)
    
  
    def add_prerequisite(course_id, prereq_id_str):
        prereq_list = [
            pid.strip()
            for pid in prereq_id_str.split(",")
            if pid.strip()
        ]

        added = []
        existed = []
        failed = []

        for prereq_id in prereq_list:
            if prereq_id == course_id:
                failed.append(prereq_id)
                continue

            result = CourseDAO.insert_prerequisite_if_not_exists(
                course_id,
                prereq_id
            )

            if result == "inserted":
                added.append(prereq_id)
            elif result == "exists":
                existed.append(prereq_id)
            else:
                failed.append(prereq_id)


        msg_parts = []

        if added:
            msg_parts.append(
                f"Added successfully: {', '.join(added)}"
            )

        if existed:
            msg_parts.append(
                f"Already existed: {', '.join(existed)}"
            )

        if failed:
            msg_parts.append(
                f"Invalid: {', '.join(failed)}"
            )

        if not msg_parts:
            msg = "No prerequisite was added."
            return False, msg

        msg = " ".join(msg_parts)
        return True, msg
    
    def edit_prerequisites(course_id, prereq_id_str):

        prereq_list = [
            pid.strip()
            for pid in prereq_id_str.split(",")
            if pid.strip()
        ]

        if not prereq_list:
            return False, "Prerequisite list is empty"

        added = []
        failed = []

        for prereq_id in prereq_list:
            if prereq_id == course_id:
                failed.append(prereq_id)

        if failed:
            return False, f"Invalid prerequisite IDs: {failed}"

        CourseDAO.delete_prerequisites_by_course(course_id)

        for prereq_id in prereq_list:
            result = CourseDAO.update_prerequisite(course_id, prereq_id)
            if result:
                added.append(prereq_id)
            else:
                failed.append(prereq_id)

        msg = "Edit prerequisite completed.\n"
        if added:
            msg += f"Added: {', '.join(added)}\n"
        if failed:
            msg += f"Failed: {', '.join(failed)}"

        return True, msg
    
    def get_prerequisites_by_course(course_id):
        return CourseDAO.get_prerequisites(course_id)
    
    def export_overview_stats():
        data = AdminDAO.get_dashboard_statistics()

        file_path = Path("system_overview.csv")

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(data.keys())
            writer.writerow(data.values())

        return True, file_path
    
    def import_academic_config(file_path):
        success = []
        failed = []

        encodings = ["utf-8-sig", "utf-8", "cp1258", "cp1252", "latin1"]
        reader = None
        file = None

        for enc in encodings:
            try:
                file = open(file_path, "r", newline="", encoding=enc)
                reader = csv.DictReader(file)

               
                if not reader.fieldnames:
                    raise UnicodeDecodeError(enc, b"", 0, 1, "Empty header")

                break  

            except UnicodeDecodeError:
                if file:
                    file.close()
                reader = None
                file = None
                continue

        if not reader:
            return False, (
                "Cannot read file.\n"
                "Please save CSV as UTF-8 or ANSI (Excel default)."
            )

        try:
            required_cols = {"academicYear", "semester", "policies"}
            if not required_cols.issubset(reader.fieldnames):
                return False, (
                    "Invalid file format.\n"
                    "Required columns:\n"
                    "academicYear, semester, policies"
                )

            for line, row in enumerate(reader, start=2):
                academic_year = row.get("academicYear", "").strip()
                semester = row.get("semester", "").strip()
                policies = row.get("policies", "").strip()

                if not academic_year or not semester:
                    failed.append(f"Row {line}: missing academicYear or semester")
                    continue

                try:
                    result = AdminController.create_academic_config(
                        academic_year,
                        semester,
                        policies
                    )

                    if result:
                        success.append(f"{semester}-{academic_year}")
                    else:
                        failed.append(f"Row {line}: duplicate config")

                except Exception as e:
                    failed.append(f"Row {line}: {e}")

            msg = (
                f"Import completed\n\n"
                f"Success: {len(success)}\n"
                f"Failed: {len(failed)}"
            )

            if failed:
                msg += "\n\nFailed details:\n" + "\n".join(failed[:10])
                if len(failed) > 10:
                    msg += f"\n... and {len(failed) - 10} more"

            return True, msg

        finally:
            if file:
                file.close()

