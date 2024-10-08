import mysql.connector
import logging
from helpers.get_file_path import get_file_path

class Database:
    '''
    Core class for all database related actions
    
    Attributes:
        config (dict): A dictionary containing the database connection parameters
        
    Examples:
        db = Database(config, connect=True, setup=True)\n
        db.query('SELECT * FROM users')
    '''
    def __init__(self, config: dict, connect: bool = True, setup: bool = False):
        self.config = config
        self.setup_file = config.get('setup_file', None)
        self.connection = self.create_connection() if connect else None
        
        if setup:
            self.setup_database()
        
    def create_connection(self) -> mysql.connector.connection.MySQLConnection:
        '''
        Creates a connection to the db, and returns the connection object
        '''
        try: 
            return mysql.connector.connect(
                host = self.config['db_host'],
                port = self.config['db_port'],
                user = self.config['db_user'],
                password = self.config['db_pass'],
                autocommit = self.config['autocommit'],
                collation = self.config.get('collation', 'utf8mb4_unicode_ci'),
                charset = 'utf8mb4',
                database = self.config.get('db_name', None)
            )
        except mysql.connector.Error as connection_error:
            logging.error(f'Error connecting to the database: {connection_error}')
            return None
    
    def close_connection(self):
        '''
        Closes the connection to the db
        '''
        try:
            self.connection.commit() # Commit any pending transactions
            self.connection.close()
            logging.info('Database connection closed')
            return True
        except Exception as error:
            logging.error(f'Error closing the database connection:\n{error}')
            return False
        
    def setup_database(self, file_path: str = None) -> bool:
        '''
        Runs the initital setup script for the db
        '''
        file_path = file_path if file_path else self.setup_file
        
        if file_path is None or file_path == '':
            logging.warning('No setup file provided')
            return False
        
        try:
            with open(get_file_path(self.setup_file), 'r', encoding='utf-8') as setup_file:
                setup_script = setup_file.read()
                self.execute_script(setup_script)
                
            tables = [table[0] for table in self.query("SHOW TABLES")]
                        
            logging.info(f'Database `{self.connection.database}` setup successfully.\nTables: {tables}')
            return True
        except Exception as error:
            logging.error(f'Error setting up the database:\n{error}')
            return False
           
    def execute_script(self, script: str):
        '''
        Executes a multi-statement SQL script
        '''
        try:
            with self.connection.cursor() as cursor:
                sql_statements = script.split(';')
                for statement in sql_statements:
                    if statement.strip():
                        cursor.execute(statement)
                        self.connection.commit()
        except Exception as error:
            logging.error(f'Error executing script:\n{error}')
            return False
             
    def query(self, query: str, values: tuple = (), fetch: bool = True, cursor_settings: dict = {}) -> dict:
        '''
        Executes singular `query` on the database
        '''
        try:
            cursor = self.connection.cursor(**cursor_settings)
            cursor.execute(query, values)
            
            data_found = cursor.fetchall()
            
            return {
                'affected_rows': cursor.rowcount,
                'result_group': True if len(data_found) > 0 else False,
                'result': data_found,
            }
        except Exception as error:
            logging.error(f'Error executing query `{query}`:\n{error}')
            return False