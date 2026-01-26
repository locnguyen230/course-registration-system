from model.db_connection import DBConnection
from datetime import date

class RegistrationDAO:

    @staticmethod
    def register(registration_id, student_id, batch_id, section_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO RegistrationRecords
                (registrationID, studentID, status, registrationDate, batchID, sectionID)
                VALUES (%s, %s, 'REGISTERED', %s, %s, %s)
            """, (
                registration_id,
                student_id,
                date.today(),
                batch_id,
                section_id
            ))

            cursor.execute("""
                UPDATE CourseSection
                SET enrolledCount = enrolledCount + 1
                WHERE sectionID = %s
            """, (section_id,))

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            print("REGISTER ERROR:", e)
            return False

        finally:
            conn.close()


    @staticmethod
    def withdraw(student_id, section_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE RegistrationRecords
            SET status = 'CANCELLED'
            WHERE studentID = %s
            AND sectionID = %s
            AND status = 'REGISTERED'
        """, (student_id, section_id))

        if cursor.rowcount == 0:
            conn.rollback()
            conn.close()
            return False

        cursor.execute("""
            UPDATE CourseSection
            SET enrolledCount = enrolledCount - 1
            WHERE sectionID = %s
            AND enrolledCount > 0
        """, (section_id,))

        conn.commit()
        conn.close()
        return True


    @staticmethod
    def is_course_completed(student_id, section_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 1
            FROM RegistrationRecords
            WHERE studentID = %s
              AND sectionID = %s
              AND status = 'COMPLETED'
        """, (student_id, section_id))

        completed = cursor.fetchone() is not None
        conn.close()
        return completed

    @staticmethod
    def generate_registration_id(major):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT MAX(registrationID)
            FROM RegistrationRecords
            WHERE registrationID LIKE %s
        """, (f"REG-{major}-%",))

        last_id = cursor.fetchone()[0]
        conn.close()

        if last_id is None:
            return f"REG-{major}-000001"

        last_number = int(last_id.split("-")[-1])
        next_number = last_number + 1

        return f"REG-{major}-{next_number:06d}"

    @staticmethod
    def get_course_regis_by_std(student_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        query = """
            SELECT
                rr.sectionID,
                c.courseName,
                rr.registrationDate
            FROM RegistrationRecords rr
            JOIN CourseSection cs ON rr.sectionID = cs.sectionID
            JOIN Course c ON cs.courseID = c.courseID
            WHERE rr.studentID = %s
            AND rr.status = 'Registered'
            ORDER BY rr.registrationDate DESC
        """

        cursor.execute(query, (student_id,))
        rows = cursor.fetchall()

        conn.close()
        return rows
