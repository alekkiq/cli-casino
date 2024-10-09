from random import shuffle
from time import sleep
from os import system, name
import GameHelpers

class Ventti:
    def __init__(self, player: dict):
        self.player = player
        self.helpers = GameHelpers.GameHelpers(player)
        self.ventti = 21
        self.max_turns = 3
        self.ranks = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K")
        self.suits = ("hearts", "diamonds", "clubs", "spades")
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.player_turn = 0
        self.dealer_turn = 0
        self.player_total = 0
        self.dealer_total = 0
        self.player_has_ace = False
        self.dealer_has_ace = False
        self.player_pass = False
        self.dealer_pass = False
        self.player_over = False
        self.dealer_over = False
        self.player_win = False

    def clear(self):
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

# Nollaa kaikki pelin arvot
    def game_stat_reset(self):
        self.deck.clear()
        self.player_hand.clear()
        self.dealer_hand.clear()
        self.player_turn = 0
        self.dealer_turn = 0
        self.player_total = 0
        self.dealer_total = 0
        self.player_has_ace = False
        self.dealer_has_ace = False
        self.player_pass = False
        self.dealer_pass = False
        self.player_over = False
        self.dealer_over = False
        self.player_win = False

# Funktio paljastaa joko pelaajan tai jakajan käden
    def hand_reveal(self):
        if not self.player_pass:
            for card in self.player_hand:
                print(f"{self.player_hand.index(card) + 1}. card of your hand is {card['rank']} of {card['suit']} ")
        else:
            for card in self.dealer_hand:
                print(f"Dealers {self.dealer_hand.index(card) + 1}. card is {card['rank']} of {card['suit']}")

# Tällä funktiolla luodaan pakka ja sekoitetaan käyttäen randomin shuffle funktiota.
    def shuffle_deck(self):
        for i in range(len(self.suits)):
            for j in range(len(self.ranks)):
                self.deck.append({"suit":self.suits[i],"rank":self.ranks[j], "value":j+1})
                shuffle(self.deck)

# Funktio jolla jaetaan kortit jakajalle ja pelaajalle. Ajetaan vain kerran pelin alussa.
    def first_deal(self):
        self.shuffle_deck()
        for i in range(2):
            self.player_hand.append(self.deck[0])
            self.deck.remove(self.deck[0])
        for i in range(2):
            self.dealer_hand.append(self.deck[0])
            self.deck.remove(self.deck[0])
        self.score_calculation()
        for card in self.player_hand:
            if card["value"] == 1 and self.player_total + 13 <= self.ventti and not self.player_has_ace:
                if input("You have an ace! Do you want it to have value of 14? Y/n ").upper() == "Y":
                    self.player_has_ace = True
        for card in self.dealer_hand:
            if card["value"] == 1 and self.dealer_total + 13 <= self.ventti and not self.dealer_has_ace:
                self.dealer_has_ace = True

# Funktio tarkistaa onko käden arvo ylittänyt ventin ja lopettaa joko pelaajan tai jakajan vuoron.
    def over_check(self):
        if self.player_over:
            self.dealer_pass = True
        if not self.player_pass:
            if self.player_total > self.ventti:
                print("Busted!")
                self.player_pass = True
                self.player_over = True
            else:
                print(f"You have total of {self.player_total}!")
        else:
            if self.dealer_total > self.ventti:
                print(f"Dealer has total of {self.dealer_total}!")
                print("Dealer busted!")
                self.dealer_pass = True
                self.dealer_over = True
            else:
                print(f"Dealer has total of {self.dealer_total}!")

# Funktio uuden kortin nostamiseen. Merkkaa myös kulkevaa vuoroa
    def hit_me(self):
        if not self.player_pass:
            if self.player_turn < self.max_turns:
                if input("Do you want a another card? Y/n: ").upper() == "Y":
                    self.player_hand.append(self.deck[0])
                    self.deck.remove(self.deck[0])
                    if self.player_hand[0]["value"] == 1 and not self.player_has_ace:
                        if self.player_total + 13 <= self.ventti:
                            print("you have following cards in your hand")
                            for card in self.player_hand:
                                print(card["rank"] + " of " + card["suit"])
                            if input("Do you want your ace to be value of 14? Y/n: ").upper() == "Y":
                                self.player_has_ace = True
                    self.player_turn += 1
                else:
                    self.player_pass = True
            else:
                self.player_pass = True
        else:
            if self.dealer_turn < self.max_turns and not self.player_over:
                if self.dealer_total < self.player_total:
                    self.dealer_hand.append(self.deck[0])
                    self.deck.remove(self.deck[0])
                    if self.dealer_hand[0]["value"] == 1 and not self.dealer_has_ace:
                        if self.dealer_total + 13 <= self.ventti:
                            self.dealer_has_ace = True
                    self.dealer_turn += 1
                else:
                    self.dealer_pass = True
            else:
                self.dealer_pass = True

# funktio jolla lasketaan pelaajan/jakajan pistetulos.
    def score_calculation(self):
        self.player_total = 0
        self.dealer_total = 0
        if self.player_has_ace:
            self.player_total += 13
        if self.dealer_has_ace:
            self.dealer_total += 13
        for p_card in self.player_hand:
            self.player_total += p_card["value"]
        for d_card in self.dealer_hand:
            self.dealer_total += d_card["value"]

# Funktio voittajan määrittelyyn.
    def is_winner(self):
        if self.player_over or self.dealer_over:
            if self.player_over:
                print("Dealer won the game!")
            else:
                print("Congratulations! You won the game!")
                self.player_win = True
        elif self.player_total == self.dealer_total:
            print("Dealer has won the game!")
        elif self.player_total <= self.dealer_total:
            print("Dealer has won the game!")
        else:
            print("Congratulations! You won the game!")
            self.player_win = True



# Pelin logiikka tulee tänne.
    def ai_logic(self):
        if not self.dealer_pass:
            if self.dealer_turn < self.max_turns:
                if self.player_over:
                    self.dealer_pass = True
                else:
                    if self.player_total <= self.dealer_total:
                        self.dealer_pass = True
                    else:
                        self.hit_me()
            else:
                self.dealer_pass = True


# Pääfunktio pelin ajamiseen.
    def run(self):
        while True:
            self.game_stat_reset()
            bet = self.helpers.getBet()
            self.first_deal()
            while not self.player_pass:
                self.hand_reveal()
                self.score_calculation()
                self.over_check()
                self.hit_me()
                self.clear()
            while not self.dealer_pass:
                self.hand_reveal()
                self.score_calculation()
                self.over_check()
                sleep(1)
                self.ai_logic()
                sleep(1)
                self.clear()
            self.is_winner()

            if self.player_win:
                self.helpers.updatePlayerBalance(bet * 2, True)
            elif not self.player_win:
                print(f"You have {self.helpers.getCurrentBalance()} credits left.")

            if not self.helpers.playAgain():
                break

if __name__ == "__main__":
    game = Ventti({'id': 2, 'username': 'Tuukka', 'balance': 125})
    game.run()