from model.db_connection import DBConnection

class UserDAO:

    @staticmethod
    def find_by_username(username):
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT userID, password, role, status
            FROM user
            WHERE userName = %s
        """
        cursor.execute(sql, (username,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()
        return user


    @staticmethod
    def find_by_id(user_id):
        conn = DBConnection.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM user WHERE userID = %s",
            (user_id,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()
        return user


    @staticmethod
    def update_password(user_id, hashed_password):
        conn = DBConnection.get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE user
            SET password = %s
            WHERE userID = %s
        """

        cursor.execute(sql, (hashed_password, user_id))
        conn.commit()

        success = cursor.rowcount > 0

        cursor.close()
        conn.close()

        return success
