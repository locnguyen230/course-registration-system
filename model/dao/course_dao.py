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
    
    @staticmethod
    def get_courses():
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT
                    c.courseID,
                    c.courseName,
                    c.credits,
                    c.description,
                    COALESCE(
                        GROUP_CONCAT(
                            cp.prerequisiteID
                            ORDER BY cp.prerequisiteID
                            SEPARATOR ', '
                        ),
                        'None'
                    ) AS prerequisites
                FROM Course c
                LEFT JOIN CoursePrerequisites cp
                    ON c.courseID = cp.courseID
                GROUP BY
                    c.courseID,
                    c.courseName,
                    c.credits,
                    c.description
                ORDER BY c.courseID;
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_max_course_number_by_major(major):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT MAX(
                CAST(SUBSTRING(courseID, %s) AS UNSIGNED)
            )
            FROM Course
            WHERE courseID LIKE %s
        """, (len(major) + 1, major + '%'))

        result = cursor.fetchone()[0]
        conn.close()

        return result 
    
    @staticmethod
    def get_course(course_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT *
                FROM Course
                WHERE courseID = %s
            """, (course_id,))

            return cursor.fetchone()

        except Exception as e:
            print("Get course error:", e)
            return None

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_course(course_id, course_name, credits, description):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO Course(courseID, courseName, credits, description)
                VALUES (%s, %s, %s, %s)
            """, (course_id, course_name, credits, description))

            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print("Insert course error:", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def update_course(course_id, course_name, credits, description):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE Course
                SET courseName = %s,
                    credits = %s,
                    description = %s
                WHERE courseID = %s
            """, (
                course_name,
                credits,
                description,
                course_id
            ))

            conn.commit()

            return cursor.rowcount > 0

        except Exception as e:
            conn.rollback()
            print("Update course error:", e)
            return False

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def insert_prerequisite_if_not_exists(course_id, prereq_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT 1
                FROM CoursePrerequisites
                WHERE courseID = %s AND prerequisiteID = %s
            """, (course_id, prereq_id))

            if cursor.fetchone():
                return "exists"

            cursor.execute("""
                INSERT INTO CoursePrerequisites (courseID, prerequisiteID)
                VALUES (%s, %s)
            """, (course_id, prereq_id))

            conn.commit()
            return "inserted"

        except Exception as e:
            conn.rollback()
            print("DAO error:", e)
            return "error"

        finally:
            conn.close()

    @staticmethod
    def delete_prerequisites_by_course(course_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM CoursePrerequisites
                WHERE courseID = %s
            """, (course_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print("DAO delete error:", e)
        finally:
            conn.close()

    @staticmethod
    def update_prerequisite(course_id, prereq_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO CoursePrerequisites (courseID, prerequisiteID)
                VALUES (%s, %s)
            """, (course_id, prereq_id))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print("DAO insert error:", e)
            return False
        finally:
            conn.close()


