import logging
import tabulate

# TODO 
# In the beginning of each while() loop add the header() function call to clear
# the terminal and print the header. For consistency.

# Most likely it will be a helper from the CLI main class.

class GameHistory:
    def __init__(self, db_handler: object, player: object):
        self.db = db_handler
        self.player = player
        
        # default amount
        self.history_rows = 100
        
        self.table_columns = [
            {
                'db_column': 'name',
                'name': 'Peli'
            },
            {
                'db_column': 'bet',
                'name': 'Panos'
            },
            {
                'db_column': 'win_amount',
                'name': 'Voitto'
            },
            {
                'db_column': 'played_at',
                'name': 'Ajankohta'
            }
        ]
        
    def get_game_history(self, amount: int) -> list:
        '''
        Gets the amount of records from the game history table
        '''
        try:
            query = f'''
                SELECT
                    game_history.bet,
                    game_history.win_amount,
                    game_history.played_at,
                    game_types.name
                FROM game_history
                JOIN game_types
                ON game_history.game_type_id = game_types.id
                WHERE game_history.user_id = {self.player.get_data().get('id')}
                ORDER BY game_history.played_at DESC
                LIMIT {amount}
            '''
            
            result = self.db.query(query, cursor_settings={'dictionary': True})
            
            if result['result_group']:
                return result['result']
        except Exception as error:
            logging.error(f'Error getting the game history: {error}')
            return []
        
    def print_table(self, data: list = []):
        '''
        Prints the game history in a table
        '''
        if len(data) == 0:
            print('Ei pelejä näytettäväksi!\n')
            return
        
        headers = [column['name'] for column in self.table_columns]
        rows = []
        
        for row in data:
            rows.append([row[column['db_column']] for column in self.table_columns])
        
        # Align the columns
        alignment = ['center'] * (len(headers) - 1)
        
        print(tabulate.tabulate(rows, headers, tablefmt='fancy_grid', colalign=alignment), '\n')
        
    def start_game_history(self):
        '''
        Starts the game history menu
        '''
        while True:
            # HEADER HERE! TODO
            
            choice = input('Montako peliä näytetään: ')
            
            if not choice.isdigit() or int(choice) < 1:
                print('Virheellinen syöte. Syötä vähintään 1.\n')
                continue
            else:
                if choice == '' or not choice:
                    choice = self.history_rows # fallback to default
                    
                data = self.get_game_history(choice)
                self.print_table(data)
                
                input('Palaa takaisin painamalla <Enter>\n')
                break