import random
from time import sleep
from .GameHelpers import GameHelpers
import shutil

class Roulette:
    '''
    Game: Roulette
    Description: The simplest form of single guess roulette, where the player chooses a number to bet on and then spins the wheel. self.colors are not included in this version, but the number multiplier is faithful, with 0 in the pool too.
    '''
    def __init__(self, player: object, db_handler: object):
        self.player = player
        self.helpers = GameHelpers(player, db_handler, 'roulette')
        
        # betting options
        self.colors = {
            'v': [0],
            'p': [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36],
            'm': [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        }
        self.color_names = {
            'p': 'punainen',
            'm': 'musta',
            'v': 'vihreä'
        }
        self.number_guesses = 2 # hard coded value for the amount of number guesses the player can make
        
        self.roll_history_rolls = 10 # the amount of rolls to keep in the history
        self.roll_history = self._create_initial_history()
        
    def _create_initial_history(self) -> list:
        history = []
        
        for i in range(self.roll_history_rolls):
            num = random.randint(0, 36)
            history.append({
                'number': num,
                'color': 'v' if num in self.colors['v'] else 'p' if num in self.colors['p'] else 'm'
            })
            
        return history
    
    def _print_history(self) -> None:
        history_str = "  |  ".join([f'{roll["number"]}-{self.color_names[roll["color"][0]][0].upper()}' for roll in self.roll_history])
        print(f'Viimeiset {self.roll_history_rolls} pyöräytystä:')
        
        self.helpers.box_wrapper(history_str)
        
    def _spin_wheel(self) -> int:
        print('\nPyörä pyörii...\n')
        
        sleep(random.randint(1 * 10, 3 * 10) / 10) # sleep for a random time between 0.5 and 1 seconds

        rolled_number = random.randint(0, 36)
        rolled_color = 'v' if rolled_number in self.colors['v'] else 'p' if rolled_number in self.colors['p'] else 'm'

        roll = {
            'number': rolled_number,
            'color': rolled_color,
        }

        # add the new roll to the history
        self.roll_history.insert(0, roll)
    
        # remove the oldest roll
        self.roll_history.pop()
        
        return roll

    def _validate_guesses(self, number_guesses, color_guess) -> bool:
        print('\n')

        # Check if at least one guess is provided
        if not number_guesses and not color_guess:
            print('Sinun tulee syöttää joko numeroarvaus tai väriarvaus.\n')
            return False

        # Validate number guesses
        for i, number_guess in enumerate(number_guesses):
            if number_guess:
                if not number_guess.isdigit():
                    print(f'Numeroarvaus {i + 1} on virheellinen. Syötä numero 0 - 36.\n')
                    return False
                if not 0 <= int(number_guess) <= 36:
                    print(f'Numeroarvaus {i + 1} on virheellinen. Syötä numero 0 - 36.\n')
                    return False

        # Validate color guess
        if color_guess and color_guess.lower() not in ['p', 'm']:
            print('Väriarvaus on virheellinen. Syötä p (punainen) tai m (musta).\n')
            return False

        return True
        
    def _determine_outcome(self, number_guesses, number_bets, color_guess, color_bet, roll: int) -> int:
        total_winnings = 0

        # Check number guesses
        for number_guess, number_bet in zip(number_guesses, number_bets):
            if number_guess.isdigit() and int(number_guess) == roll['number']:
                total_winnings += number_bet * 36

        # Check color guess
        if color_guess is not None and color_guess == roll['color']:
            total_winnings += color_bet * 2

        return total_winnings
        
    def start_game(self) -> object:
        '''
        Runs the game and returns the player object when done
        '''
        while True:
            # TODO Header / terminal reload here!!!
            # eg. header('Ruletti', self.player.get_balance())
            
            self.helpers.game_intro(self.player.get_username())
            
            # print the last 20 rolls (randomly created at this point of time, will get updated when the game is played)
            self._print_history()    
            
            color_guess = input(f'\nVäriarvaus\nSyötä tyhjä, jos arvaat vain numeroa. (p/m): ')
            number_guesses = [input(f'\nNumeroarvaus {i+1}\nSyötä tyhjä, jos arvaat vain väriä.\n(0 - 36): ') for i in range(2)]

            if not self._validate_guesses(number_guesses, color_guess):
                sleep(3) # wait for a few seconds before continuing, so the player can read the error messages
                continue

            # get separate bets for each guess
            if not any(number_guesses): # if no number guesses, ask for a color bet
                number_bets = [0, 0]
                color_bet = self.helpers.get_bet(self.player.get_balance(), 'Panos väriarvaukselle')
            else:
                number_bets = [self.helpers.get_bet(self.player.get_balance(), f'Panos numeroarvaukselle {i+1} ({number_guesses[i]})') for i in range(2)]
                color_bet = self.helpers.get_bet(self.player.get_balance(), 'Panos väriarvaukselle')

            total_bet = sum(number_bets) + color_bet

            if total_bet == 0: # allow the player to exit the game before betting
                break

            roll = self._spin_wheel()
            print(f'\nPyörä pyörähti! Numero: {roll["number"]}, väri: {self.color_names[roll["color"]]}\n')
            
            outcome = self._determine_outcome(number_guesses, number_bets, color_guess, color_bet, roll)
            game_won = outcome > 0

            # print the right outcome message
            if game_won:
                # check which guess was correct
                if color_guess == roll['color'] and not any(number_guess == str(roll['number']) for number_guess in number_guesses):
                    print(f'\nVäriarvaus oli oikein! Voitit {outcome - total_bet} pistettä!\n')
                elif any(number_guess == str(roll['number']) for number_guess in number_guesses) and not color_guess == roll['color']:
                    print(f'\nNumeroarvaus oli oikein! Voitit {outcome} pistettä!\n')
                else:
                    print(f'\nMolemmat arvauksesi olivat oikein! Voitit {outcome} pistettä!\n')
            else:
                print(f'\nArvaukset menivät pieleen. Parempi onni ensi kerralla!\n')
                
            # Bulk-update the player values
            self.helpers.update_player_values(game_won, outcome, save = True)
            
            # Save the game to the database
            self.helpers.save_game_to_history(bet = total_bet, win_amount = outcome)
            
            if not self.helpers.play_again(self.player.get_balance()):
                break

        return self.player