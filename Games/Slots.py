import random
import time

# Here we make a list of symbols that the slot machine will use. graphemica.com is a good place to find them.
# Currently, we have 5 different symbols and as a result, the chance of winning jackpot is 0.8%.
# Chance for 3 matching symbols is 12.8%.
symbols = ['🍑', '🍌', '🍒', '🍏', '🍇']
# This is the main function that runs the slot(s?) machine.
# It takes two parameters: 'spins_per_column' determines how many times each column will spin before the symbol
# is chosen, and 'columns' is here to determine how many rows of symbols we should print.
def slots_game(spins_per_column = 4, columns = 4):
    # First we calculate the total number of spins we need for the game.
    total_spins = spins_per_column * columns
    # We create an empty list (with an empty string inside, multiplied by the amount of columns we have)
    # that we use for keeping track of the final row to determine potential winnings.
    final_row = [''] * columns
    # Next we run through this loop as many times as we have our total_spin set to.
    for s in range(total_spins):
        # We create an empty list to store the symbols we need to print next.
        row_to_print = []
        # Next we loop through each column to determine the row that we will print
        for c in range(columns):
            # Columns lock after they have spun "spins_per_column" times. Starting from the left-most column.
            # For example first column will lock after it has spun (0 + 1) * 4 times and second after it has spun
            # (1 + 1) * 4 times.

            # We check if the column in question is locked or not based on what is the number of spins we've had so far.
            # In other words, the value of s
            if s >= (c + 1) * spins_per_column:
                # If the value of s is big enough for this column to have been locked, then instead of getting a
                # random new symbol we take the corresponding symbol from our final_row instead and add it to
                # the row we want to print.
                row_to_print.append(final_row[c])
            else:
                # We choose a random new symbol for the column.
                new_symbol = random.choice(symbols)
                # We add the newly chosen symbol to the row we will be printing next.
                row_to_print.append(new_symbol)
                # This checks to see if the current spin count is 1 spin before the column should be locked.
                # Meaning that this would be the final spin for the column in question.
                if s == (c + 1) * spins_per_column - 1:
                    # If the condition is true, the new_symbol that was last chosen  is assigned to final_row
                    # and the column is now "officially" locked and will no longer change after this spin
                    # as we will be using the symbol saved in final_row instead.
                    final_row[c] = new_symbol
        # Next we use the join function to take the list with its [] and ' ' and turn it into
        # a nice and clean string that shows up only as symbols without any of the extra "baggage" and print it.
        print(' '.join(row_to_print))
        # We use time.sleep to make sure there is a delay before each row is printed.
        # The delay gets bigger after each quarter of total spins for that "authentic slot(s?) machine feel".
        if s < (total_spins/4):
            time.sleep(0.3)
        elif s < (total_spins/2):
            time.sleep(0.4)
        elif s < (total_spins * 0.75):
            time.sleep(0.5)
        else:
            time.sleep(0.6)

    # Once we have completed the spinning loops we will print the final result one more time to make it clear.
    print("Your final result is:", ' '.join(final_row))

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
        print("You win the Jackpot")
    # If there was 3 of the same symbol, the player gets a smaller win.
    elif 3 in symbol_counts.values():
        print("3 matches. You win!")
    # Otherwise they don't win anything.
    else:
        print("Better luck next time!")

if __name__ == "__main__":
    slots_game()

# TODO: (Actual important stuff, non-optional):
#   1. Connect Slots game to the rest of the casino 'system" so it can be ran from the main UI.
#   2. Set up the ability to track and modify the database of player's balance and winnings.
#   3. Other integrations if/as necessary.

# TODO: (Just some ideas floating in my head, doesn't mean im actually going to do all of them)
#   1. Explore the possibility of only showing 3 rows at a time and replacing the old rows rather than
#      printing more and more new lines. - LOW Priority
#   2. Make the middle of the 3 rows to be the winning row in the end. - LOW Priority
#   3. Make the rows appear faster at the beginning and slow down as we get closer to the final row.
#      You know, like a real slot(s?) machine. Or is it the wheel of fortune i'm thinking about... - Done
#   4. Make each symbol be worth different amount of winnings. - LOW Priority
#   5. Possibility of winning with only 3 out of 4 being the same symbol. Is that a 'thing' in real slot machines?
#      I've never used a slot machine in my life. - Done
#   6. Replace one of the yellow symbols with something else. Too.Much.Yellow! - Done
