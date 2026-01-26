from model.db_connection import DBConnection

class CourseDAO:

    @staticmethod
    def get_open_courses():
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                c.courseID,
                c.courseName,
                c.credits,
                (cs.capacity - cs.enrolledCount) AS available
            FROM Course c
            JOIN CourseSection cs ON c.courseID = cs.courseID
        """)

        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def search_courses(keyword):
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        like = f"%{keyword.lower()}%"

        query = """
            SELECT
                c.courseID,
                c.courseName,
                c.credits,
                (cs.capacity - cs.enrolledCount) AS available
            FROM Course c
            JOIN CourseSection cs ON c.courseID = cs.courseID
            WHERE LOWER(c.courseName) LIKE %s
            OR LOWER(c.courseID) LIKE %s
        """

        cursor.execute(query, (like, like))
        result = cursor.fetchall()

        conn.close()
        return result


    @staticmethod
    def get_prerequisites(course_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT prerequisiteID
            FROM CoursePrerequisites
            WHERE courseID = %s
        """, (course_id,))

        prereqs = [r[0] for r in cursor.fetchall()]
        conn.close()
        return prereqs

    @staticmethod
    def search_courses_registration(student_id):
        major_code = student_id[:2].lower() + "%"

        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                cs.sectionID,                     
                c.courseID,                      
                c.courseName,
                (cs.capacity - cs.enrolledCount) AS available,
                GROUP_CONCAT(cp.prerequisiteID) AS prerequisites
            FROM CourseSection cs
            JOIN Course c 
                ON cs.courseID = c.courseID
            LEFT JOIN CoursePrerequisites cp
                ON c.courseID = cp.courseID
            WHERE LOWER(c.courseID) LIKE %s
            GROUP BY
                cs.sectionID,
                c.courseID,
                c.courseName,
                cs.capacity,
                cs.enrolledCount
        """, (major_code,))

        results = cursor.fetchall()
        conn.close()
        return results


