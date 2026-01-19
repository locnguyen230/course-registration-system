import mysql.connector
from model.entities.instructor import Instructor
from model.entities.course_section import CourseSection
from model.entities.student import Student
# Lưu ý: Bạn cần đảm bảo file db_connection.py đã tồn tại
# Nếu chưa có, hãy xem hướng dẫn ở mục 2 bên dưới
try:
    from model.db_connection import get_db_connection
except ImportError:
    # Fallback nếu bạn để file config ở chỗ khác
    from config.db_config import get_db_connection

class InstructorDAO:
    def __init__(self):
        self.conn = get_db_connection()

    def get_instructor_by_user_id(self, user_id):
        cursor = self.conn.cursor(dictionary=True)
        query = "SELECT * FROM Instructor WHERE userID = %s"
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Instructor(row['instructorID'], row['fullName'], row['department'], row['userID'])
        return None

    def get_sections_by_instructor(self, instructor_id):
        cursor = self.conn.cursor(dictionary=True)
        query = "SELECT * FROM CourseSection WHERE instructorID = %s"
        cursor.execute(query, (instructor_id,))
        rows = cursor.fetchall()
        cursor.close()
        
        sections = []
        for row in rows:
            sections.append(CourseSection(
                row['sectionID'], row['sectionCode'], row['semester'], 
                row['capacity'], row['enrolledCount'], row['schedule'], 
                row['courseID'], row['instructorID']
            ))
        return sections

    def get_students_in_section(self, section_id):
        cursor = self.conn.cursor(dictionary=True)
        query = """
            SELECT s.* FROM Student s
            JOIN RegistrationRecords r ON s.studentID = r.studentID
            WHERE r.sectionID = %s AND r.status = 'REGISTERED'
        """
        cursor.execute(query, (section_id,))
        rows = cursor.fetchall()
        cursor.close()

        students = []
        for row in rows:
            students.append(Student(
                row['studentID'], row['fullName'], row['email'], 
                row['major'], row['yearLevel'], row['academicStatus'], row['userID']
            ))
        return students

    def get_pending_waitlist_requests(self, instructor_id):
        cursor = self.conn.cursor(dictionary=True)
        query = """
            SELECT w.waitlistID, s.fullName, s.studentID, c.sectionCode, w.requestDate, w.status
            FROM WaitlistRecords w
            JOIN CourseSection c ON w.sectionID = c.sectionID
            JOIN Student s ON w.studentID = s.studentID
            WHERE c.instructorID = %s AND w.status = 'WAITING'
        """
        cursor.execute(query, (instructor_id,))
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def update_waitlist_status(self, waitlist_id, new_status):
        cursor = self.conn.cursor()
        try:
            query = "UPDATE WaitlistRecords SET status = %s WHERE waitlistID = %s"
            cursor.execute(query, (new_status, waitlist_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()