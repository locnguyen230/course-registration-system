from model.db_connection import DBConnection
from datetime import datetime

class RegistrationBatchDAO:

    @staticmethod
    def get_time(student_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT
                rb.batchID,
                rb.startTime,
                rb.endTime
            FROM student s
            JOIN registrationbatch rb
                ON s.yearLevel = rb.eligibleYearLevel
            WHERE s.studentID = %s
            AND rb.startTime <= NOW()
            AND rb.endTime >= NOW()
            LIMIT 1
        """

        cursor.execute(query, (student_id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row   
    
    @staticmethod
    def get_batch_id(student_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                rb.batchID
            FROM Student s
            JOIN RegistrationBatch rb
                ON s.yearLevel = rb.eligibleYearLevel
            WHERE s.studentID = %s
            AND rb.startTime <= NOW()
            AND rb.endTime >= NOW()
            ORDER BY rb.startTime DESC
            LIMIT 1
        """, (student_id,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return row["batchID"]

        return None


