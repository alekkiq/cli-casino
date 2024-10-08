import random
from .GameHelpers import GameHelpers

class Dice:
    '''
    Game: Dice
    Description: The simplest dice game, where the player determines the number of sides on the dice and then guesses a value of the rolled dice.
    '''
    def __init__(self, player: object, db_handler: object):
        self.player = player
        self.helpers = GameHelpers(player, db_handler, 'dice')
        self.sides = 6 # default value

    def _roll_dice(self) -> int:
        return random.randint(1, self.sides)

    def _determine_outcome(self, guess: int, roll: int, bet: int) -> int:
        return bet * self.sides if guess == roll else 0

    def start_game(self) -> object:
        '''
        Runs the game and returns the player object when done
        '''
        while True:
            self.helpers.game_intro(self.player.get_username())
            
            # check if the player wants to play the game or not
            if not self.helpers.play_game():
                break
            
            # get the bet, amount of sides & the guess
            bet = self.helpers.get_bet(self.player.get_balance())
            
            # one more opportunity to exit the game before rolling the dice
            if bet == 0:
                break
            
            self.sides = self.helpers.validate_input('\nKuinka monta sivua nopassa on (2 - 20): ', 'int', 2, 20)
            guess = self.helpers.validate_input(f'\nArvaa nopan arvo (1 - {self.sides}): ', 'int', 1, self.sides)
            
            roll = self._roll_dice()
            
            outcome = self._determine_outcome(guess, roll, bet)
            game_won = outcome > 0
            net_outcome = outcome - bet

            if game_won:
                print(f'\nOnnittelut! Arvasit oikein! Voitit {outcome} pistettä!\n')
            else:
                print(f'\nHävisit pelin. Oikea arvo oli {roll}.\n')
                
            # Bulk-update the player values
            self.helpers.update_player_values(game_won, net_outcome, save = True)
            
            # Save the game to the database
            self.helpers.save_game_to_history(bet = bet, win_amount = net_outcome)
            
            if not self.helpers.play_again(self.player.get_balance()):
                break

        return self.player # return the updated player object