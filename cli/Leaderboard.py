import logging
import tabulate

# TODO 
# In the beginning of each while() loop add the header() function call to clear
# the terminal and print the header. For consistency.

# Most likely it will be a helper from the CLI main class.

class Leaderboard:
    def __init__(self, db_handler: object):
        self.db = db_handler
        
        self.leaderboard_rows = 10  
        self.filter_options = [
            {
                'db_column': 'total_winnings',
                'name': 'Kokonaisvoitot (pisteet)'
            },
            {
                'db_column': 'games_played',
                'name': 'Pelatut pelit'
            },
            {
                'db_column': 'games_won',
                'name': 'Voitetut pelit'
            },
            {
                'db_column': 'games_lost',
                'name': 'Hävityt pelit'
            },
            {
                'db_column': None,
                'name': 'Palaa päävalikkoon\n'
            }
        ]
        
    def get_filtered_data(self, filter_column: str, sort: str = 'DESC'):
        '''
        Executes the query to get the filtered data from the db based on the user's choice
        '''
        try:
            query = f'''
                SELECT 
                    users.username,
                    user_statistics.total_winnings,
                    user_statistics.games_played,
                    user_statistics.games_won,
                    user_statistics.games_lost
                FROM users
                JOIN user_statistics
                ON users.id = user_statistics.user_id
                ORDER BY {filter_column} {sort}
                LIMIT {self.leaderboard_rows}
            ''' 
            
            result = self.db.query(query, cursor_settings={'dictionary': True})
            
            if result['result_group'] > 0: # if there are results
                return result['result']
        except Exception as error:
            logging.error(f'Error getting the filtered leaderboard: {error}')
            return []
        
    def determine_sort_order(self) -> str:
        '''
        Determines the sort order based on the user's choice
        '''
        while True:
            # HEADER HERE! TODO
            
            sort_orders = [
                'Laskeva',
                'Nouseva\n',
                'Peruuta\n'
            ]
            
            print('Valitse tulostaulun järjestys:\n')
            
            for index, order in enumerate(sort_orders, start = 1):
                print(f'{index})  {order}')
            
            sort_choice = int(input(f'Syötä valintasi (1 - {len(sort_orders)}): '))
            
            match sort_choice:
                case 1:
                    return 'DESC'
                case 2:
                    return 'ASC'
                case 3:
                    break
                case _:
                    return 'DESC'
                
    def print_table(self, data: list, filter: str, sort_order: str = 'DESC') -> None:
        '''
        Prints the leaderboard table
        '''
        
        headers = ['#', 'Käyttäjänimi'] + [option['name'] for option in self.filter_options if option['db_column']] + ['Voitto-%']
        rows = []
        
        for index, row in enumerate(data, start=1):
            win_percentage = (row['games_won'] / row['games_played'] * 100) if row['games_played'] > 0 else 0
            rows.append([index] + list(row.values()) + [f"{win_percentage:.2f}%"])
        
        # Align the columns
        alignment = ['center', 'left'] + ['center'] * (len(headers) - 2)
        
        print(tabulate.tabulate(rows, headers, tablefmt='fancy_grid', colalign=alignment))
        print(f'10 parasta pelaajaa "{filter}" mukaan {"laskevassa" if sort_order == "DESC" else "nousevassa"} järjestyksessä\n')
        
    def start_leaderboard(self):
        '''
        The main method to run the leaderboard
        '''
        
        while True:
            # HEADER HERE! TODO
            
            print('Valitse haluamasi järjestyskriteeri:\n')
            
            for index, option in enumerate(self.filter_options, start = 1):
                print(f'{index})  {option.get("name")} {"\n" if option == self.filter_options[-2] else ""}')

            filter_choice = int(input(f'Syötä valintasi (1 - {len(self.filter_options)}): '))
            
            if filter_choice == len(self.filter_options): # back to main menu
                break
            elif filter_choice in range(1, len(self.filter_options)):
                filter_column = self.filter_options[filter_choice - 1].get('db_column')
                sort_order = self.determine_sort_order()
                
                data = self.get_filtered_data(filter_column, sort_order)

                self.print_table(data, self.filter_options[filter_choice - 1].get('name'), sort_order)
                
                input('Palaa takaisin painamalla <Enter>\n')
                continue
            else: # invalid choice
                print(f'Virheellinen valinta! Valitse numerolla 1 - {len(self.filter_options)}\n')
                continue