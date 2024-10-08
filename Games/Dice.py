import random
from .GameHelpers import GameHelpers

class Dice:
    '''
    Game: Dice
    Description: The simplest dice game, where the player determines the number of sides on the dice and then guesses a value of the rolled dice.

    Examples:
        dice_game = Dice({'id': 2, 'username': 'John', 'balance': 125})\n
        dice_game.startGame()
    Attributes:
        player (str): The name of the player
        rules (str): The rules of the game
        sides (int): The number of sides on the dice
        max_dice (int): The maximum number of dice that can be rolled
        dice_sum (int): The sum of the dice rolls
    '''
    def __init__(self, player: object, db_handler: object):
        self.player = player
        self.helpers = GameHelpers(player, db_handler, 'dice')
        self.sides = 6 # default value

    def _roll_dice(self) -> int:
        return random.randint(1, self.sides)

    def _determine_outcome(self, guess: int, roll: int, bet: int) -> int:
        return bet * self.sides if guess == roll else 0

    def start_game(self) -> dict:
        '''
        Runs the game and returns the player object when done
        '''
        while True:
            # TODO Header / terminal reload here!!!
            # eg. header('Nopanheitto', self.player.get_balance())
            self.helpers.game_intro(self.player.get_username())

            bet = self.helpers.get_bet(self.player.get_balance())
            self.sides = int(input(f'Montako sivua nopassa on: '))

            if self.sides < 2:
                print('Nopassa on oltava yli 2 sivua. Syötä muu luku.\n')
                continue

            guess = int(input(f'Syötä arvauksesi (1 - {self.sides}): '))
            roll = self._roll_dice()
            
            outcome = self._determine_outcome(guess, roll, bet)
            net_winnings = outcome - bet
            game_won = outcome > 0

            if outcome > 0:
                print(f'\nOnnittelut! Arvasit oikein! Voitit {net_winnings} pistettä!\n')
            else:
                print(f'\nHävisit pelin. Oikea arvo oli {roll}.\n')
                
            # Bulk-update the player values
            self.helpers.update_player_values(game_won, outcome, save = True)
            
            # Save the game to the database
            self.helpers.save_game_to_history(bet = bet, win_amount = outcome)
            
            if not self.helpers.play_again(self.player.get_balance()):
                break

        return self.player # return the updated player object