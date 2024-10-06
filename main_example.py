from config import config
from Database import Database
from Player import Player

from cli.Leaderboard import Leaderboard
from cli.GameHistory import GameHistory

from Games.Dice import Dice

logo = r"""
  ____  _      ___    ____     _     ____  ___  _   _   ___
 / ___|| |    |_ _|  / ___|   / \   / ___||_ _|| \ | | / _ \
| |    | |     | |  | |      / _ \  \___ \ | | |  \| || | | |
| |___ | |___  | |  | |___  / ___ \  ___) || | | |\  || |_| |
 \____||_____||___|  \____|/_/   \_\|____/|___||_| \_| \___/
"""

def main():
    db_configs = config()
    db = Database(
        config = db_configs, 
        connect = True, 
        setup = True
    )
    
    clear_terminal()
    
    # auth loop
    while True:
        name = input('Käyttäjänimesi: ')
        password = input('Salasana: ')

        try:
            player = Player(name, password, db)
            break
        except Exception as error:
            print(f'Virheellinen salasana! Yritä uudelleen.\n')
    
    # The main menu (1st level loop)
    while True:
        header(f'Tervetuloa, {player.get_username()}', player.get_balance())
        
        main_menu = [
            'Tulostaulukot',
            'Oma pelihistoria',
            'Käyttäjäasetukset',
            'Poistu pelistä\n',
        ]
        
        if player.get_balance() > 0 and not player.get_ban_status():
            main_menu.insert(0, 'Pelivalikko\n') # allow the player to do other things, but play games.
        
        for index, choice in enumerate(main_menu, start = 1):
            print(f'{index})  {choice}')
        
        choice = int(input(f'\nValitse (1 - {len(main_menu)}): '))
        
        match choice:
            case 1: # game selection
                game_menu = (
                    'Nopanheitto',
                    # jne.
                    'Palaa päävalikkoon\n',
                )
                
                # Sub menu, eg. game selection (2nd level loop)
                while True:
                    header('Valitse peli', player.get_balance())
                    
                    # 2nd level loop -> eg. game selection
                    for index, game in enumerate(game_menu, start=1):
                        print(f'{index})  {game}')
                            
                    game_choice = int(input(f'\nValitse peli (1 - {len(game_menu)}): '))
                    
                    match game_choice:
                        case 1: # dice
                            header('Nopanheitto', player.get_balance())
                            
                            dice_game = Dice(player, db)
                            dice_game.start_game()
                        case 2: # back to main menu
                            break
                        case _:
                            print(f'Virheellinen valinta! Valitse numerolla {game_menu[0]} - {game_menu[-1]}')
                # ...
            case 2:
                header('Tulostaulukot', player.get_balance())
                
                leaderboard = Leaderboard(db)
                leaderboard.start_leaderboard()
            case 3:
                header('Oma pelihistoria', player.get_balance())
                
                game_history = GameHistory(db, player)
                game_history.start_game_history()
            case 5: # TODO dynamically get the last index
                print(f'\nNäkemiin, {player.get_username()}!')
                player.save() # save the player's data once more before exiting
                break
            case _: # incorrect input
                print(f'Virheellinen valinta! Valitse numerolla {main_menu[0]} - {main_menu[-1]}')
    
# helpers
def clear_terminal():
    '''
    Clears the terminal, and prints the logo
    '''
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{logo}\n')
    
def header(text: str, balance: int) -> None:
    '''
    Prints the header. Call this on the start of each loop
    '''
    clear_terminal()
    return print(f'{text}  |  Saldo: {balance}\n\n')

if __name__ == '__main__':
    main() # Run the app