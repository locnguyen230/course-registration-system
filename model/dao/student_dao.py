from model.db_connection import DBConnection

class StudentDAO:

    @staticmethod
    def get_student_by_id(student_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT studentID, fullName, major,
                   yearLevel, academicStatus
            FROM Student
            WHERE studentID = %s
        """, (student_id,))

        student = cursor.fetchone()
        conn.close()
        return student

    @staticmethod
    def is_active_student(student_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT academicStatus
            FROM Student
            WHERE studentID = %s
        """, (student_id,))

        row = cursor.fetchone()
        conn.close()

        return row and row[0] == "ENROLLED"

    @staticmethod
    def get_year_level(student_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT yearLevel
            FROM Student
            WHERE studentID = %s
        """, (student_id,))

        row = cursor.fetchone()
        conn.close()

        return row[0] if row else None

    @staticmethod
    def get_completed_courses(student_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT cs.courseID
            FROM RegistrationRecords r
            JOIN CourseSection cs ON r.sectionID = cs.sectionID
            WHERE r.studentID = %s AND r.status = 'COMPLETED'
        """, (student_id,))

        completed = [r[0] for r in cursor.fetchall()]
        conn.close()
        return completed
    
    @staticmethod
    def get_student_by_user_id(user_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT *
            FROM student
            WHERE userID = %s
        """
        cursor.execute(sql, (user_id,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()
        return result
