import logging
import tabulate
import sys

class PlayerProfile:
    def __init__(self, db_handler: object, player: object):
        self.db = db_handler
        self.player = player
        
    def _profile_menu(self) -> tuple:
        return (
            'Omat statistiikat',
            'Muuta käyttäjätietoja\n', # change name, password or delete account
            'Palaa päävalikkoon\n',
        )
        
    def __get_stats(self) -> list:
        '''
        Gets the player statistics from the user_statistics table
        '''
        try:
            query = f'''
                SELECT
                    user_statistics.total_winnings as 'Kokonaisvoitot (pisteet)',
                    user_statistics.games_played as 'Pelatut pelit',
                    user_statistics.games_won as 'Voitetut pelit',
                    user_statistics.games_lost as 'Hävityt pelit',
                    CASE
                        WHEN user_statistics.is_banned = 0 THEN 'Ei'
                        WHEN user_statistics.is_banned = 1 THEN 'Kyllä'
                    END as 'Porttikiellossa'
                FROM user_statistics
                WHERE user_id = {self.player.get_data().get('id')}
            '''
            
            result = self.db.query(query, cursor_settings={'dictionary': True})
            
            if result['result_group']:
                return result['result']
            else: # practically cant happen since there is atleast the default data
                return []
        except Exception as error:
            logging.error(f'Error getting the player stats: {error}')
            return []
    
    def _show_stats(self, data: list = []):
        '''
        Prints the player statistics in a table
        '''
        if len(data) == 0:
            print('Ei näytettäviä tilastoja.\n')
            return
        
        headers = data[0].keys()
        rows = [list(row.values()) for row in data]
        
        alignment = ['center'] * len(headers)
        
        print(tabulate.tabulate(rows, headers, tablefmt='fancy_grid', colalign=alignment), '\n')
  
    def start_player_profile(self):
        '''
        Starts the player profile view
        '''
        while True:
            # HEADER HERE! TODO
            
            profile_menu = self._profile_menu()
            
            for index, choice in enumerate(profile_menu, start = 1):
                print(f'{index})  {choice}')
            
            menu_choice = int(input(f'\nValitse (1 - {len(profile_menu)}): '))
            
            match menu_choice:
                case 1:
                    player_stats = self.__get_stats()
                    self._show_stats(player_stats)
                    
                    input('Palaa takaisin painamalla <Enter>\n')
                    continue
                case 2:
                    profile_update_menu = (
                        'Vaihda käyttäjänimi',
                        'Vaihda salasana',
                        'Poista käyttäjä\n',
                        'Kumoa porttikielto\n',
                        'Takaisin\n',
                    )
                    
                    for index, choice in enumerate(profile_update_menu, start = 1):
                        print(f'{index})  {choice}')
                        
                    update_choice = int(input(f'\nValitse (1 - {len(profile_update_menu)}): '))
                    
                    match update_choice:
                        case 1:
                            new_name = input('Syötä uusi käyttäjänimi: ')
                            
                            if not new_name:
                                print('Virheellinen syöte!\n')
                                continue
                            else:
                                if self.player.update_username(new_name):
                                    print('Käyttäjänimi vaihdettu.\n')
                                else:
                                    print('Käyttäjänimen vaihto epäonnistui.\n')
                        case 2:
                            new_password = input('Syötä uusi salasana: ')
                            
                            if not new_password:
                                print('Virheellinen syöte!\n')
                                continue
                            else:
                                if self.player.update_password(new_password):
                                    print('Salasana vaihdettu.\n')
                                else:
                                    print('Salasanan vaihto epäonnistui.\n')
                        case 3:
                            confirm = input('Haluatko varmasti poistaa käyttäjän? (k/e): ')
                            
                            if confirm.lower() == 'k':
                                if self.player.delete_account():
                                    print('Käyttäjä poistettu.\n')
                                    print('Kiitos peliemme pelaamisesta!\n')
                                    
                                    sys.exit() # just close the program, we dont allow unauthorized access
                            else:
                                print('Käyttäjä ei poistettu.\n')
                        case 4:
                            if self.player.get_ban_status() == 1:
                                balance_to_return = int(input('Syötä palautettava saldo (max. 1000): '))
                                
                                if balance_to_return > 1000 or balance_to_return < 1:
                                    print('Virheellinen summa! Syötä 1 - 1000\n')
                                    continue
                                
                                if self.player.unban_account(balance_to_return):
                                    print(f'Porttikielto poistettu. Saldoa lisätty {balance_to_return}\n')
                                else:
                                    print('Porttikiellon poisto epäonnistui.\n')
                            else:
                                print('Käyttäjä ei ole porttikiellossa!\n')
                        case 5:
                            print(self.player.get_data())
                            self.player.save()
                            print(self.player.get_data())
                            # break
                        case _:
                            print(f'Virheellinen valinta! Valitse numerolla 1 - {len(profile_update_menu)}\n')
                case 3:
                    break
                case _:
                    print(f'Virheellinen valinta! Valitse numerolla 1 - {len(profile_menu)}\n')