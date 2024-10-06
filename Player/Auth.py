import logging
import hashlib

class Auth:
    def __init__(self, db_handler: object):
        self.__db = db_handler
        
    def create_user(self, username: str, password: str) -> bool:
        '''
        Handles new user creation in the db "users" table
        '''
        try:
            hashed_password = self.__hash_password(password)
            
            insert_query = '''
                INSERT INTO users (username, password)
                VALUES (%s, %s)
            '''
            
            self.__db.query(insert_query, (username, hashed_password))
            self.__db.connection.commit()
            
            created_user_id = self.__db.query('SELECT LAST_INSERT_ID() AS id')['result'][0][0]
            
            logging.info(f'User `{username}` created with id {created_user_id}')
            
            return {
                'id': created_user_id,
                'username': username,
                'password': hashed_password
            }
        except Exception as error:
            logging.error(f'Error creating user: {error}')
            return False
        
    def authenticate_user(self, username: str, password: str) -> bool:
        '''
        Authenticates the user against the db "users" table
        '''
        try:
            hashed_password = self.__hash_password(password)
            
            query = '''
                SELECT id, username, password 
                FROM users
                WHERE username = %s AND password = %s
            '''
            
            result = self.__db.query(query, (username, hashed_password), cursor_settings={'dictionary': True})

            if result['result_group']:
                user = result['result'][0]
                if self.__verify_password(password, user['password']):
                    logging.info(f'User `{username}` authenticated successfully')
                    return {
                        'id': user['id'],
                        'username': user['username'],
                        'password': user['password']
                    }
                else:
                    logging.warning(f'Password verification failed for user `{username}`')
                    return False
            else:
                return False
        except Exception as error:
            logging.error(f'User `{username}` authentication failed.\nError: {error}')
            return False
        
    def check_user_exists(self, username: str) -> bool:
        '''
        Checks if the user exists in the db "users" table
        '''
        try:
            query = '''
                SELECT id, username
                FROM users
                WHERE username = %s
            '''
            
            result = self.__db.query(query, (username,))
            
            if result['result_group']:
                return True
            else:
                return False
        except Exception as error:
            logging.error(f'Error checking if user exists: {error}')
            return False
        
    def __hash_password(self, password: str) -> str:
        '''
        Hashes of the password given (sha256)
        '''
        return hashlib.sha256(password.encode()).hexdigest()
    
    def __verify_password(self, password: str, hashed_password: str) -> bool:
        '''
        Verifies the password against the hashed password
        '''
        return self.__hash_password(password) == hashed_password