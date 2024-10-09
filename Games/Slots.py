import random
import time
from .GameHelpers import GameHelpers

class Slots:
    # We start by initializing the Slots class with player information and game settings.
    # First we have the player object which contains information such as the player's account balance.
    # Next we have db_handler which is needed for things such as saving the game results.
    # 'spins_per_column' determines how many times each column will spin before the symbol is chosen.
    # 'columns' is here to determine how many columns of symbols we should print.
    def __init__(self, player: object, db_handler: object, spins_per_column=4, columns=4):
        self.player = player
        self.helpers = GameHelpers(player, db_handler, 'slots')
        # We store tje spins_per_column and columns as attributes of the class.
        # So they can be used outside the __init__ method.
        self.spins_per_column = spins_per_column
        self.columns = columns
        # Here we make a list of symbols that the slot machine will use. graphemica.com is a good place to find them.
        # Currently, we have 5 different symbols and as a result, the chance of winning jackpot is 0.8%.
        # Chance for 3 matching symbols is 12.8%.
        self.symbols = ['🍑', '🍌', '🍒', '🍏', '🍇']

    # This is the method to spin the slot machine rows and columns.
    def _spin_reels(self) -> list:
        # First we calculate the total number of spins we need for the game.
        total_spins = self.spins_per_column * self.columns
        # We create an empty list (with an empty string inside, multiplied by the amount of columns we have).
        # We use it for keeping track of the final row to determine potential winnings.
        final_row = [''] * self.columns
        # Next we run through this loop as many times as we have our total_spins set to.
        for s in range(total_spins):
            row_to_print = []
            for c in range(self.columns):
                # Columns lock after they have spun "spins_per_column" times. Starting from the left-most column.
                # For example first column will lock after it has spun (0 + 1) * 4 times and second after it has spun
                # (1 + 1) * 4 times.

                # We check if the column in question is locked or not based on what is the number of spins we've had so far.
                # In other words, the value of s.
                if s >= (c + 1) * self.spins_per_column:
                    # If the value of s is big enough for this column to have been locked, then instead of getting a
                    # random new symbol we take the corresponding symbol from our final_row instead and add it to
                    # the row we want to print.
                    row_to_print.append(final_row[c])
                else:
                    # We choose a random new symbol for the column.
                    new_symbol = random.choice(self.symbols)
                    # We add the newly chosen symbol to the row we will be printing next.
                    row_to_print.append(new_symbol)
                    # This checks to see if the current spin count (value of s) is 1 spin before the column should be locked.
                    # Meaning that this would be the final spin for the column in question.
                    if s == (c + 1) * self.spins_per_column - 1:
                        # If the condition is true, the new_symbol that was last chosen  is assigned to final_row
                        # and the column is now "officially" locked and will no longer change after this spin
                        # as we will be using the symbol saved in final_row instead.
                        final_row[c] = new_symbol
            # Next we use the join function to take the list with its [] and ' ' and turn it into
            # a nice and clean string that shows up only as symbols without any of the extra "baggage" and print it.
            print(' '.join(row_to_print))
            # We use time.sleep inside the _delay_spin method to make sure there is a delay before each row is printed.
            self._delay_spin(s, total_spins)
        # Once we have completed the spinning loops we will print the final result one more time to make it clear.
        print("Lopullinen tuloksesi on:", ' '.join(final_row))
        return final_row
    # Method used to add delay to spins.
    def _delay_spin(self, current_spin: int, total_spins: int) -> None:
        # The delay gets bigger after each quarter of total spins for that "authentic slot machine feel".
        if current_spin < (total_spins / 4):
            time.sleep(0.3)
        elif current_spin < (total_spins / 2):
            time.sleep(0.4)
        elif current_spin < (total_spins * 0.75):
            time.sleep(0.5)
        else:
            time.sleep(0.6)

    # This method will determine if the player has won something or not by checking the final_row for potential matches.
    def _determine_outcome(self, final_row: list) -> int:
        # We make an empty dictionary to count how many of each different symbol there is in the final row.
        symbol_counts = {}
        # We loop through each symbol in the final_row
        for symbol in final_row:
            # If the symbol is already in the dictionary, increase its count
            if symbol in symbol_counts:
                symbol_counts[symbol] += 1
            else:
                # If the symbol is not in the dictionary, add it with a count of 1
                symbol_counts[symbol] = 1

        # If the count of a symbol is 4 it means all symbols were the same and player wins the jackpot
        if 4 in symbol_counts.values():
            print("Voitit jättipotin!")
            return 250
        # If there was 3 of the same symbol, the player gets a smaller win.
        elif 3 in symbol_counts.values():
            print("Onnitelut, 3 vastaavaa symbolia!")
            return 50
        # Otherwise they don't win anything.
        else:
            #print("Parempaa onnea ensi kerralla!")
            return 0

    # The "main" method that runs the Slot machine's game loop.
    def start_game(self) -> object:

        while True:
            self.helpers.game_intro(self.player.get_username())
            # If the player doesn't want to play the game we break (their legs). Also known as exiting the game.
            if not self.helpers.play_game():
                break
            # The cost of using the slot machine.
            bet = 10
            # Here we call the _spin_reels to run the slot machine.
            final_row = self._spin_reels()
            # Here we determine if player won something.
            outcome = self._determine_outcome(final_row)
            net_outcome = outcome - bet
            game_won = net_outcome > 0
            # We inform the player of their winnings, if they had any.
            if game_won:
                print(f'\nOnnittelut! Voitit {outcome} pistettä!\n')
            else:
                print(f'\nHävisit. Parempaa onnea ensi kerralla!\n')

            # We update the game_helpers stuff to save the game history in the database.
            self.helpers.update_player_values(game_won, net_outcome, save=True)
            self.helpers.save_game_to_history(bet=bet, win_amount=net_outcome)

            if not self.helpers.play_again(self.player.get_balance()):
                break
        # We return the updated player object with changes to their casino balance.
        return self.player
