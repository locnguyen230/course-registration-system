from model.db_connection import DBConnection
from datetime import datetime

class WaitlistDAO:

    @staticmethod
    def generate_waitlist_id(major):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT MAX(waitlistID)
            FROM WaitlistRecords
            WHERE waitlistID LIKE %s
        """, (f"WAIT-{major}-%",))

        last_id = cursor.fetchone()[0]
        conn.close()

        if last_id is None:
            return f"WAIT-{major}-000001"

        last_number = int(last_id.split("-")[-1])
        next_number = last_number + 1

        return f"WAIT-{major}-{next_number:06d}"
    
    @staticmethod
    def get_next_position(section_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(MAX(position), 0) + 1
            FROM WaitlistRecords
            WHERE sectionID = %s
              AND status = 'WAITING'
        """, (section_id,))

        position = cursor.fetchone()[0]
        conn.close()
        return position

    @staticmethod
    def add_to_waitlist(waitlist_id, student_id, section_id, position):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO WaitlistRecords
        (waitlistID, studentID, sectionID, requestDate, position, status)
        VALUES (%s, %s, %s, %s, %s, 'WAITING')
        """
        cursor.execute(query, (
            waitlist_id,
            student_id,
            section_id,
            datetime.now(),
            position
        ))

        conn.commit()
        conn.close()

    @staticmethod
    def get_waitlist_status(student_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT
            w.sectionID,
            c.courseID,
            c.courseName,
            w.status,
            w.position
        FROM waitlistrecords w
        JOIN coursesection cs ON w.sectionID = cs.sectionID
        JOIN course c ON cs.courseID = c.courseID
        WHERE w.studentID = %s
        ORDER BY w.position
        """, (student_id,))

        result = cursor.fetchall()
        conn.close()
        return result
