import bcrypt
from model.dao.user_dao import UserDAO
from model.dao.student_dao import StudentDAO
from model.dao.instructor_dao import InstructorDAO
from model.dao.admin_dao import AdminDAO


class AuthController:

    # AUTHENTICATE USER
    @staticmethod
    def authenticate(username, password):
        user = UserDAO.find_by_username(username)

        if not user:
            return False, "Invalid username or password"

        if user["status"] != "ACTIVE":
            return False, "Account is inactive"


        if not bcrypt.checkpw(
            password.encode(),
            user["password"].encode()
        ):
            return False, "Invalid username or password"
        
        if user["role"] == "STUDENT":
            student = StudentDAO.get_student_by_user_id(user["userID"])
            user["studentID"] = student["studentID"]
            user["yearLevel"] = student["yearLevel"]
        elif user["role"] == "INSTRUCTOR":
            instructor = InstructorDAO.get_instructor_by_user_id(user["userID"])
            user["instructorID"] = instructor["instructorID"]
        elif user["role"] == "ADMIN":
            admin = AdminDAO.get_admin_by_user_id(user["userID"])
            user["adminID"] = admin["adminID"]
        return True, user


    # CHANGE PASSWORD (UC-S7)
    @staticmethod
    def change_password(user_id, old_password, new_password):
        user = UserDAO.find_by_id(user_id)

        if not bcrypt.checkpw(
            old_password.encode(),
            user["password"].encode()
        ):
            return False, "Current password is incorrect"

        if len(new_password) < 8:
            return False, "Password must be at least 8 characters"

        hashed_password = bcrypt.hashpw(
            new_password.encode(),
            bcrypt.gensalt()
        ).decode()

        success = UserDAO.update_password(user_id, hashed_password)

        if not success:
            return False, "Failed to update password"

        return True, "Password changed successfully"
