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


    @staticmethod
    def get_all():
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT *
            FROM RegistrationBatch
        """

        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result
    
    @staticmethod
    def get_by_batchid(batch_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT *
            FROM RegistrationBatch
            WHERE batchID = %s
        """

        cursor.execute(query, (batch_id,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result
    
    @staticmethod
    def get_next_batch_id():
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT batchID
                FROM RegistrationBatch
            """)
            rows = cursor.fetchall()

            max_number = 0

            for (batch_id,) in rows:
                # lấy số ở cuối
                num = ""
                for ch in reversed(batch_id):
                    if ch.isdigit():
                        num = ch + num
                    else:
                        break

                if num:
                    max_number = max(max_number, int(num))

            return max_number + 1

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def insert_batch(batch_id, semester, start_time, end_time, eligible_year):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO RegistrationBatch (
                    batchID,
                    semester,
                    startTime,
                    endTime,
                    eligibleYearLevel
                )
                VALUES (%s, %s, %s, %s, %s)
            """, (
                batch_id,
                semester,
                start_time,
                end_time,
                eligible_year
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
    def update_batch(batch_id, semester, start_time, end_time, eligible_year):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE RegistrationBatch
                SET semester = %s,
                    startTime = %s,
                    endTime = %s,
                    eligibleYearLevel = %s
                WHERE batchID = %s
            """, (
                semester,
                start_time,
                end_time,
                eligible_year,
                batch_id
            ))

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            print(e)
            return False

        finally:
            cursor.close()
            conn.close()

