import oracledb
from config.db_config import DB_CONFIG
from utils.hash_utils import hash_password


class UserModel:
    def __init__(self):
        """Initialize the UserModel for database operations."""
        self.db_config = DB_CONFIG

    def create_user(self, name, email, password, profile_picture_url, bio):
        """
        Create a new user profile in the database.

        Args:
            name (str): The user's name.
            email (str): The user's email.
            password (str): The plain text password to be hashed and stored.
            profile_picture_url (str): URL of the user's profile picture.
            bio (str): The user's biography.

        Returns:
            bool: True if the user was created successfully, False otherwise.
        """
        hashed_password = hash_password(password)
        try:
            with oracledb.connect(**self.db_config) as connection:
                cursor = connection.cursor()
                cursor.execute('''
                    INSERT INTO users (name, email, password_hash, profile_picture_url, bio)
                    VALUES (:1, :2, :3, :4, :5)
                ''', (name, email, hashed_password, profile_picture_url, bio))
                connection.commit()
                return True
        except oracledb.DatabaseError as e:
            print(f"Database error during user creation: {e}")
            return False

    def get_user_info(self, email, password):
        """
        Authenticate a user by checking their email and password hash.

        Args:
            email (str): The user's email.
            password (str): The plain text password entered by the user.

        Returns:
            dict: {user_id (int), name (str)} if the credentials are valid
            False (bool) otherwise.
        """
        hashed_password = hash_password(password)
        try:
            with oracledb.connect(**self.db_config) as connection:
                cursor = connection.cursor()
                cursor.execute('''
                    SELECT user_id, name FROM users WHERE email = :1 AND password_hash = :2
                ''', (email, hashed_password))
                result = cursor.fetchone()
                cursor.close()
                connection.close()

            if result:
                return {"user_id": result[0], "name": result[1]}
            else:
                return None
        except oracledb.DatabaseError as e:
            print(f"Database error during authentication: {e}")
            return False

    def get_spaces_info(self):
        '''

        '''
        try:
            with oracledb.connect(**self.db_config) as connection:
                cursor = connection.cursor()
                cursor.execute('''
                    SELECT space_id, name FROM spaces
                ''')
                result = cursor.fetchall()

                space_infos = []
                for space in result:
                    cursor.execute('''
                        SELECT COUNT(*) FROM events WHERE space_id = :1
                    ''', (space[0],))
                    event_count = cursor.fetchone()
                    cursor.execute('''
                        SELECT congestion_level FROM congestion_reports WHERE space_id = :1
                        ORDER BY reported_at DESC
                    ''', (space[0],))
                    latest_report = cursor.fetchone()
                    space_infos.append({
                        "id": space[0],
                        "name": space[1],
                        "event_count": event_count[0],
                        "latest_report": latest_report[0]
                    })

                cursor.close()
                connection.close()

            return space_infos
        except oracledb.DatabaseError as e:
            print(f"Database error during authentication: {e}")
            return False

    def get_events_info(self, selected_space):
        '''

        '''
        try:
            with oracledb.connect(**self.db_config) as connection:
                cursor = connection.cursor()
                cursor.execute('''
                    SELECT event_id, title, start_time, end_time FROM events
                    WHERE space_id = :1
                ''', (selected_space["id"],))
                result = cursor.fetchall()

                events_info = []
                for event in result:
                    cursor.execute('''
                        SELECT user_id FROM event_participants
                        WHERE event_id = :1
                    ''', (event[0],))
                    participant_ids = cursor.fetchall()
                    participant_ids = tuple(row[0] for row in participant_ids)

                    if participant_ids:
                        query = f'''
                            SELECT name FROM users
                            WHERE user_id IN
                            ({', '.join([':{}'.format(i+1) for i in range(len(participant_ids))])})
                        '''
                        cursor.execute(query, participant_ids)
                        participant_names = tuple(row[0] for row in cursor.fetchall())
                    else:
                        participant_names = None

                    events_info.append({
                        "id": event[0],
                        "title": event[1],
                        "start_time": event[2],
                        "end_time": event[3],
                        "participant_ids": participant_ids,
                        "participant_names": participant_names
                    })

                cursor.close()
                connection.close()

            return events_info
        except oracledb.DatabaseError as e:
            print(f"Database error during authentication: {e}")
            return False

    def join_event(self, event_id, user_id):
        '''
        '''
        try:
            with oracledb.connect(**self.db_config) as connection:
                cursor = connection.cursor()
                cursor.execute('''
                    INSERT INTO event_participants (event_id, user_id, joined_at)
                    VALUES (:1, :2, CURRENT_TIMESTAMP)
                ''', (event_id, user_id))
                connection.commit()
                return True
        except oracledb.DatabaseError as e:
            print(f"Database error during user creation: {e}")
            return False

    def quit_event(self, event_id, user_id):
        '''
        '''
        try:
            with oracledb.connect(**self.db_config) as connection:
                cursor = connection.cursor()
                cursor.execute('''
                    DELETE FROM event_participants WHERE
                    event_id = :1 AND user_id = :2
                ''', (event_id, user_id))
                connection.commit()
                return True
        except oracledb.DatabaseError as e:
            print(f"Database error during user creation: {e}")
            return False

    def create_event(self, space_id, organizer_id, title, description, start_time, end_time):
        '''
        '''
        try:
            with oracledb.connect(**self.db_config) as connection:
                cursor = connection.cursor()
                cursor.execute('''
                    INSERT INTO events (space_id, organizer_id, title, description, start_time, end_time) VALUES
                    (:1, :2, :3, :4,
                    TO_TIMESTAMP(:5, 'YYYY-MM-DD HH24:MI:SS.FF6'), TO_TIMESTAMP(:6, 'YYYY-MM-DD HH24:MI:SS.FF6'))
                ''', (space_id, organizer_id, title, description, start_time, end_time))
                connection.commit()
                return True
        except oracledb.DatabaseError as e:
            print(f"Database error during user creation: {e}")
            return False