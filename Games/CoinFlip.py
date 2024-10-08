import random
from time import sleep
from .GameHelpers import GameHelpers

class CoinFlip:
    def __init__(self, player: object, db_handler: object):
        self.player = player
        self.helpers = GameHelpers(player, db_handler, 'coinflip')
        
        self.coin_sides = [
            ('k', 'kruuna', '👑'),
            ('c', 'klaava', '🍀'),         
        ]
        
    def _flip_coin(self) -> str:
        return random.choice(self.coin_sides)
    
    def _determine_outcome(self, guess: str, flip: str, bet: int) -> int:
        return bet * 2 if guess == flip[0] else 0
    
    def start_game(self) -> object:
        '''
        Runs the game and returns the player object when done
        '''
        while True:
            self.helpers.game_intro(self.player.get_username())
            
            # check if the player wants to play the game or not
            if not self.helpers.play_game():
                break
            
            bet = self.helpers.get_bet(self.player.get_balance())
            
            # one more opportunity to exit the game before flipping the coin
            if bet == 0:
                break
            
            guess = self.helpers.validate_input('\nArvaa kruuna vai klaava (k/c): ', 'str', 'k', 'c')
            
            flip = self._flip_coin()
            print(f'\nKolikonheiton tulos: {flip[1]} {flip[2]}\n')
            
            outcome = self._determine_outcome(guess, flip, bet)
            game_won = outcome > 0
            net_outcome = outcome - bet
            
            if game_won:
                print(f'\nOnnittelut! Arvasit oikein! Voitit {outcome} pistettä!\n')
            else:
                print(f'\nHävisit pelin.\n')
            
            # Bulk-update the player values
            self.helpers.update_player_values(game_won, net_outcome, save = True)
            
            # Save the game to the database
            self.helpers.save_game_to_history(bet = bet, win_amount = net_outcome)
            
            if not self.helpers.play_again(self.player.get_balance()):
                break
            
        return self.player