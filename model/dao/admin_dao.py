from model.db_connection import DBConnection

class AdminDAO:

    @staticmethod
    def get_admin_by_user_id(user_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM administration
            WHERE userID = %s
        """, (user_id,))

        admin = cursor.fetchone()
        conn.close()
        return admin
    
    @staticmethod
    def get_dashboard_statistics():
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                (SELECT COUNT(*) FROM student)        AS students,
                (SELECT COUNT(*) FROM instructor)     AS instructors,
                (SELECT COUNT(*) FROM course)         AS courses,
                (SELECT COUNT(*) FROM coursesection) AS sections,
                (SELECT COUNT(*) FROM registrationrecords)   AS registrations
        """)

        stats = cursor.fetchone()
        conn.close()
        return stats
    
    @staticmethod
    def get_info_student(student_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                s.studentID,
                u.username,
                s.fullName,
                s.email,
                u.status,
                s.academicStatus
            FROM student s
            JOIN user u ON s.userID = u.userID
            WHERE s.studentID = %s
        """, (student_id,))

        student = cursor.fetchone()

        cursor.close()
        conn.close()

        return student
    
    @staticmethod
    def get_all_student():
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                s.studentID,
                u.username,
                s.fullName
            FROM student s
            JOIN user u ON s.userID = u.userID 
            WHERE u.status = "ACTIVE"
        """)

        liststd = cursor.fetchall()
        conn.close()
        return liststd
    
    @staticmethod
    def get_user_id_by_student_id(student_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT userID FROM student WHERE studentID = %s",
            (student_id,)
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row[0]
    
    @staticmethod
    def update_student_info(user_id, fullName, email, academic_status):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE student
                SET fullName = %s,
                    email = %s,
                    academicStatus = %s
                WHERE userID = %s
            """, (
                fullName,
                email,
                academic_status,
                user_id
            ))

            conn.commit()
            return True

        except Exception as e :
            conn.rollback()
            print(e)
            return False

        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def update_user_info(user_id, username, password):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        try:
            if password:
                cursor.execute("""
                    UPDATE user
                    SET username = %s,
                        password = %s
                    WHERE userID = %s
                """, (username, password, user_id))
            else:
                cursor.execute("""
                    UPDATE user
                    SET username = %s,
                        status = %s
                    WHERE userID = %s
                """, (username, user_id))

            conn.commit()
            return True
        except Exception:
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    

    @staticmethod
    def get_next_student_number_by_major(major):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) 
            FROM student
            WHERE major = %s
        """, (major.upper(),))

        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return count + 1
    
    
    @staticmethod
    def add_new_user(user_id, username, password, role, status):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO user (userID, username, password, role, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                user_id,
                username,
                password,
                role,
                status
            ))

            conn.commit()
            return True

        except Exception:
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_new_student(student_id, full_name, email, major, year_level, academic_status, user_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO student (
                    studentID,
                    fullName,
                    email,
                    major,
                    yearLevel,
                    academicStatus,
                    userID
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                student_id,
                full_name,
                email,
                major,
                year_level,
                academic_status,
                user_id
            ))

            conn.commit()
            return True

        except Exception:
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_student_by_userid(user_id, status):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE user
                SET status = %s
                WHERE userID = %s
            """, (
                status,
                user_id
            ))

            conn.commit()
            return True

        except Exception:
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_info_config():
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM academicconfiguration
        """)

        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result
    
    @staticmethod
    def add_new_config(config_id, academic_year, semester, policies):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO academicconfiguration
                (configID, academicYear, semester, policies)
                VALUES (%s, %s, %s, %s)
            """, (
                config_id,
                academic_year,
                semester,
                policies
            ))

            conn.commit()
            return True

        except Exception as e:
            print("ADD CONFIG ERROR:", e)
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()
    

    @staticmethod
    def update_config(config_id, academic_year, semester, policies):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE academicconfiguration
                SET academicYear = %s,
                    semester = %s,
                    policies = %s
                WHERE configID = %s
            """, (
                academic_year,
                semester,
                policies,
                config_id
            ))

            conn.commit()

            # Không có bản ghi nào bị update
            if cursor.rowcount == 0:
                return False

            return True

        except Exception as e:
            print("UPDATE CONFIG ERROR:", e)
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()

    def get_config_by_id(config_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM academicconfiguration
            WHERE configID = %s
        """, (config_id,))

        config = cursor.fetchone()

        cursor.close()
        conn.close()

        return config
