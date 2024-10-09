import logging
from datetime import datetime
import shutil

class GameHelpers:
    '''
    Helpers: Setup some common game methods that can be used across different games. Should be only used within the game classes.

    Attributes:
        player (dict): The current player object
    '''
    def __init__(self, player: object, db_handler: object, game_type_name: str):
        self.player = player # the whole class with the methods included
        self.db = db_handler
        self.game_type_record = self.__get_game_type_record(key = 'name_en', value = game_type_name)
        self.game_info = {
            'name': self.game_type_record.get('name'),
            'rules': self.game_type_record.get('rules')
        }
        
    # --------------------
    # Game related methods
    # --------------------
    def play_game(self):
        '''
        Before starting the main loop, asks the player if they want to play the game
        '''
        play_game = input(f'Haluatko pelata peliä (k / e): ').lower()
        
        match play_game:
            case 'k':
                return True
            case 'e':
                return False
            case _:
                print('Virheellinen syöte. Syötä k tai e.')
                return self.play_game()

    def validate_input(self, prompt: str, input_type: str, min_value: int = None, max_value: int = None, allowed_values: tuple = None, allow_empty: bool = False):
        '''
        Validates the input based on the type and constraints provided
        '''
        while True:
            input_value = input(prompt)
            
            if allow_empty and input_value == '':
                return None
            
            if input_type == 'int':
                try:
                    value = int(input_value)
                    if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                        print(f'\nArvon on oltava {min_value} - {max_value}\n')
                    else:
                        return value
                except ValueError:
                    print('\nVirheellinen syöte! Syötä numero!\n')
            
            elif input_type == 'str':
                if allowed_values and input_value.lower() not in allowed_values:
                    print(f'\nValinnan on oltava {"/".join(allowed_values)}.')
                else:
                    return input_value.lower()
            
            else:
                print('Syötteen tyyppi on virheellinen.\n')
            
    def get_bet(self, balance: int, bet_to_text: str = None) -> int:
        if not bet_to_text:
            bet = input(f'\nTämänhetkinen saldo: {balance}\nPanos (syötä tyhjä peruuttaaksesi): ')
        else:
            bet = input(f'\nTämänhetkinen saldo: {balance}\n{bet_to_text} (syötä tyhjä peruuttaaksesi): ')

        if bet == '' or int(bet) == 0:
            return 0
        
        if not bet.isdigit():
            print('\nVirheellinen syöte. Syötä numero.\n')
            return self.get_bet(balance)
        
        bet = int(bet)
        
        if bet <= balance:
            self.player.update_balance(-bet)
            return bet
        else:
            print(f'Saldosi on vajaa! Syötä sopiva määrä.\nSaldo: {self.player.get_balance()}')
            return self.get_bet(balance)
        
    def play_again(self, balance: str) -> bool:
        if balance <= 0:
            print(f'Saldo ei riitä. Peli päättyi.\n')
            return False
    
        prompt = str(input('Pelataanko uudestaan (k / e): ')).lower()

        match prompt:
            case 'k':
                return True
            case 'e':
                return False
            case _:
                print(f'Virheellinen syöte. Syötä k tai e.')
                return self.play_again(balance)
    
    def game_intro(self, username: str):
        print(f'Tervetuloa {self.game_info.get("name")}-peliin, {username}!\n\n')
        print(f'Pelin säännöt:')
        self.box_wrapper(self.game_info.get('rules'))
        
    def box_wrapper(self, text: str, min_width: int = 75, max_width: int = 75):
        '''
        Creates a nice box-like wrapper for a wanted text.
        Used in displaying the game rules, for example
        
        Could be located elsewhere tho - TODO
        '''
        terminal_width = shutil.get_terminal_size().columns
        padding = 4 # padding on both sides
        
        # fix the max width to the terminal width
        if terminal_width < max_width:
            max_width = terminal_width - padding
        
        paragraphs = text.split('\n')
        wrapped_lines = []

        for paragraph in paragraphs:
            words = paragraph.split()
            current_line = ""

            for word in words:
                if len(current_line) + len(word) + 1 <= max_width:
                    current_line += (word + " ")
                else:
                    wrapped_lines.append(current_line.strip())
                    current_line = word + " "
            wrapped_lines.append(current_line.strip())

        # determine the width of the box
        box_width = max(max(len(line) for line in wrapped_lines) + padding, min_width)

        print('+' + '-' * box_width + '+')

        for line in wrapped_lines:
            print(f'| {line.ljust(box_width - padding//2)} |')

        print('+' + '-' * box_width + '+\n')
    
    # ------------------------
    # Database related methods
    # ------------------------
    def __get_game_type_record(self, key: str = 'name_en', value: str = None):
        '''
        Creates a new game type in the database. References the class name as the game type name
        '''
        try:
            query = '''
                SELECT * FROM game_types WHERE {} = %s
            '''.format(key)
            
            result = self.db.query(query, (value,), cursor_settings={'dictionary': True})
            
            if result['result_group']:
                game_type_record = result['result'][0]
                return game_type_record
            else:
                return False
        except Exception as error:
            logging.error(f'Error creating the game type: {error}')
            return False
    
    def update_player_values(self, won: bool, win_amount = int, save = True):
        '''
        Updates all the player values in bulk after a game has ended
        
        @param won: bool: Whether the player won the game or not
        @param win_amount: int: The amount the player won
        @param save: bool: Whether to save the updated values to the database or not
        '''
        if won: # win
            self.player.update_total_winning(win_amount)
            self.player.update_games_won()
        else: # loss
            self.player.update_games_lost()
            
            if self.player.get_balance() <= 0:
                self.player.update_balance(0) # dont allow negative balances
                self.player.set_banned()

        self.player.update_games_played()
        self.player.update_balance(win_amount)
        
        if save: # save the updated values to the database
            self.player.save()
    
    def save_game_to_history(self, win_amount: int, bet: int) -> bool:
        '''
        Saves the game to the database. Returns success state boolean
        '''
        try:
            query = '''
                INSERT INTO game_history
                (bet, win_amount, played_at, user_id, game_type_id)
                VALUES (%s, %s, %s, %s, %s)
            '''
            
            user_id = self.player.get_data().get('id')
            game_type_id = self.db.query('SELECT id FROM game_types WHERE name = %s', (self.game_info.get('name'),), cursor_settings={'dictionary': True})['result'][0].get('id')

            values = (bet, win_amount, datetime.now(), int(user_id), int(game_type_id))
            
            result = self.db.query(query, values)
            
            if result['affected_rows'] > 0:
                return True
            else:
                raise Exception('Unexpected error saving the game')
        except Exception as error:
            logging.error(f'Error saving the game: {error}')
            return False