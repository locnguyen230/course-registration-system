from model.db_connection import DBConnection

class InstructorDAO:

    @staticmethod
    def get_instructor_by_user_id(user_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM instructor
            WHERE userID = %s
        """, (user_id,))

        instructor = cursor.fetchone()
        conn.close()
        return instructor
    
    @staticmethod
    def view_class_list(instructor_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT
                cs.sectionID,
                c.courseID,
                c.courseName,
                cs.sectionCode,
                cs.semester,
                cs.capacity,
                cs.enrolledCount,
                (cs.capacity - cs.enrolledCount) AS available
            FROM CourseSection cs
            JOIN Course c ON cs.courseID = c.courseID
            WHERE cs.instructorID = %s
            ORDER BY c.courseID
        """

        cursor.execute(query, (instructor_id,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result
    
    @staticmethod
    def view_student_in_section(section_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT
                s.studentID,
                s.fullName,
                s.email
            FROM RegistrationRecords rr
            JOIN Student s
                ON rr.studentID = s.studentID
            WHERE rr.sectionID = %s
            AND rr.status = 'REGISTERED'
            ORDER BY s.studentID
        """

        cursor.execute(query, (section_id,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result
    
    @staticmethod
    def get_requests(instructor_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT
                w.waitlistID,
                s.studentID,
                s.fullName,
                s.email,
                w.sectionID,
                w.status
            FROM WaitlistRecords w
            JOIN Student s
                ON w.studentID = s.studentID
            JOIN CourseSection cs
                ON w.sectionID = cs.sectionID
            WHERE cs.instructorID = %s
            AND w.status = 'WAITING'
        """

        cursor.execute(query, (instructor_id,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def get_waitlist(waitlist_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                w.waitlistID,
                w.studentID,
                w.sectionID,
                w.status,
                w.position,

                c.courseID,
                c.courseName,

                GROUP_CONCAT(cp.prerequisiteID SEPARATOR ',') AS prerequisite
            FROM WaitlistRecords w
            JOIN Student s ON w.studentID = s.studentID
            JOIN CourseSection cs ON w.sectionID = cs.sectionID
            JOIN Course c ON cs.courseID = c.courseID
            LEFT JOIN CoursePrerequisites cp ON c.courseID = cp.courseID
            WHERE w.waitlistID = %s
            GROUP BY
                w.waitlistID,
                w.studentID,
                w.sectionID,
                w.status,
                c.courseID,
                c.courseName
        """, (waitlist_id,))

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result

    # ===============================
    # Update waitlist status
    # ===============================
    @staticmethod
    def update_waitlist_status(waitlist_id, status):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE WaitlistRecords
            SET status = %s
            WHERE waitlistID = %s
        """, (status, waitlist_id))

        conn.commit()
        cursor.close()
        conn.close()



    # ===============================
    # Increase enrolled count
    # ===============================
    @staticmethod
    def increase_capacity(section_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE CourseSection
            SET 
                capacity = capacity + 1
            WHERE sectionID = %s
        """, (section_id,))

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update_waitlist_position(section_id, position):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE WaitlistRecords
            SET position = position - 1
            WHERE sectionID = %s
            AND status = 'WAITING'
            AND position > %s
        """, (section_id, position))

        conn.commit()
        cursor.close()
        conn.close()
