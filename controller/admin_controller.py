import uuid
import bcrypt
from datetime import datetime, time
from model.dao.admin_dao import AdminDAO
from model.dao.registration_batch_dao import RegistrationBatchDAO

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