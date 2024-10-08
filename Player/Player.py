import mysql.connector
import logging
import hashlib
from Player.Auth import Auth

class Player:
    '''
    Holds the player's data in a temporary Class, and handles the player's data manipulation.
    The current class is used to update the player's data in the database after/during each singular game.
    '''
    def __init__(self, username: str, password: str, db_handler: object):
        self.__db = db_handler
        self.__auth = Auth(db_handler)
        
        self.__username = username
        self.__password = password
        
        self.__data = self.__authenticate_or_create_user()

    # Authentication
    def __authenticate_or_create_user(self):
        user = self.__auth.authenticate_user(self.__username, self.__password)

        if user:
            return self.__load_profile(self.__username, self.__password)
        else:
            existing_user = self.__auth.check_user_exists(self.__username)
            
            if existing_user:
                raise ValueError("Incorrect password for existing user.")
            else:
                return self.__create_profile(self.__username, self.__password)

    # Getters
    def get_data(self) -> dict:
        return self.__data
    
    def get_balance(self) -> int:
        '''
        Needed so frequently that it's worth having a separate method for it
        '''
        return int(self.__data.get('balance'))
    
    def get_username(self) -> str:
        '''
        As is this
        '''
        return self.__data.get('username')
    
    def get_ban_status(self) -> bool:
        '''
        1: banned, 0: not banned
        '''
        return self.__data.get('is_banned')

    # Setters
    def update_total_winning(self, amount: int):
        self.__data['total_winnings'] += amount

    def update_games_played(self):
        self.__data['games_played'] += 1
    
    def update_games_won(self):
        self.__data['games_won'] += 1
    
    def update_games_lost(self):
        self.__data['games_lost'] += 1
    
    def update_balance(self, amount: int):
        self.__data['balance'] += amount
        
    def set_banned(self):
        self.__data['is_banned'] = True

    # Db methods
    def __load_profile(self, username: str, password: str):
        '''
        Handles loading the player's data from the database, if username matches
        '''
        try:
            authenticated = self.__auth.authenticate_user(username, password)
            
            if not authenticated:
                return False
            
            user_query = '''
                SELECT * FROM users 
                WHERE username = %s
            '''
            profile_query = '''
                SELECT * FROM user_statistics 
                WHERE user_id = %s
            '''
            
            user_result = self.__db.query(user_query, (username,), cursor_settings={'dictionary': True})
            
            if not user_result['result_group']:
                return False
            else:
                user_data = user_result['result'][0]
                
                profile_result = self.__db.query(profile_query, (user_data['id'],), cursor_settings={'dictionary': True})
                profile_data = profile_result['result'][0]
                
                return {**user_data, **profile_data} # Merge user and profile data
        except mysql.connector.Error as error:
            logging.error(f'Error loading player {username} data: {error}')
            return False

    def __create_profile(self, username: str, password: str):
        '''
        Handles creating a new player in the database
        '''
        new_user = self.__auth.create_user(username, password)
        
        if not new_user:
            return False
        
        try:
            query = '''
                INSERT INTO user_statistics 
                    (user_id)
                VALUES (%s)
            '''
            
            self.__db.query(query, (new_user['id'],))
            self.__db.connection.commit()
            
            logging.info(f'Player `{username}:{new_user['id']}` created successfully')
            
            return self.__load_profile(username, password)
        
        except mysql.connector.Error as error:
            logging.error(f'Error creating player {username} data: {error}')
            self.__db.connection.rollback()
            return False
    
    def update_username(self, new_name: str):
        '''
        Updates the player's username in the database
        '''
        try:
            query = '''
                UPDATE users SET username = %s WHERE id = %s
            '''
            values = (new_name, self.get_data().get('id'))
            
            result = self.__db.query(query, values)
            
            if result['affected_rows'] > 0:
                self.__data['username'] = new_name
                return True
            else:
                return False
        except Exception as error:
            logging.error(f'Error updating the username of user {self.get_data().get('id', None)}: {error}')
            return False
        
    def update_password(self, new_password: str):
        '''
        Updates the player's password in the database
        '''
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
    
        try:
            query = '''
                UPDATE users SET password = %s WHERE id = %s
            '''
            values = (hashed_password, self.get_data().get('id'))
            
            result = self.__db.query(query, values)
            
            if result['affected_rows'] > 0:
                self.__data['password'] = hashed_password
                return True
            else:
                return False
        except Exception as error:
            logging.error(f'Error updating the password of user {self.get_data().get('id', None)}: {error}')
            return False
    
    def delete_account(self):
        '''
        Deletes the player's profile from the database
        '''
        try:
            query_values = (self.get_data().get('id'),)
            self.__db.begin_transaction()
            
            # first, delete the user's statistics
            query_stats = '''
                DELETE FROM user_statistics WHERE user_id = %s
            '''
            
            self.__db.query(query_stats, query_values)
            
            # then delete the user's game_history
            query_history = '''
                DELETE FROM game_history WHERE user_id = %s
            '''
            self.__db.query(query_history, query_values)
            
            # theeen at last delete the user itself
            query_user = '''
                DELETE FROM users WHERE id = %s
            '''
            result = self.__db.query(query_user, query_values)
            
            self.__db.commit_transaction()
            
            if result['affected_rows'] > 0:
                return True
            else:
                return False
        except Exception as error:
            self.__db.rollback_transaction() # go back if we encounter an issue
            logging.error(f'Error deleting the user {self.get_data().get("id", None)}: {error}')
            return False
        
    def unban_account(self, balance_to_set: int):
        '''
        Unbans the player's account
        '''
        try:
            query = '''
                UPDATE user_statistics 
                SET 
                    is_banned = 0,
                    balance = %s
                WHERE user_id = %s
            '''
            values = (balance_to_set, self.get_data().get('id'))
            result = self.__db.query(query, values)
            
            if result['affected_rows'] > 0:
                self.__data['is_banned'] = False
                self.__data['balance'] = balance_to_set
                return True
            else:
                return False
        except Exception as error:
            logging.error(f'Error unbanning the user {self.get_data().get("id", None)}: {error}')
            return False
        
    def save(self):
        '''
        Used for saving the player's data from the temp object to the database
        '''
        try:
            user_query = '''
                UPDATE users 
                SET username = %s, password = %s
                WHERE id = %s
            '''
            
            profile_query = '''
                UPDATE user_statistics 
                SET balance = %s, total_winnings = %s, games_played = %s, games_won = %s, games_lost = %s, is_banned = %s
                WHERE user_id = %s
            '''
            
            user_values = (
                self.__data['username'],
                self.__data['password'],
                self.__data['id']
            )
            
            profile_values = (
                self.__data['balance'],
                self.__data['total_winnings'],
                self.__data['games_played'],
                self.__data['games_won'],
                self.__data['games_lost'],
                self.__data['is_banned'],
                self.__data['id']
            )
            
            self.__db.query(user_query, user_values)
            self.__db.query(profile_query, profile_values)
            self.__db.connection.commit()
            
            logging.info(f'Player {self.__data["id"]} data saved successfully')
        except mysql.connector.Error as error:
            logging.error(f'Error saving player {self.__data["id"]} data: {error}')
            self.__db.connection.rollback()
            return False