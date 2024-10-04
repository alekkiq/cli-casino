from config import config
from Database import Database
from Player import Player

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
        setup = False
    )
    
    clear_terminal()
    
    name = str(input('Pelaajanimesi: '))
    # TODO password input & validation

    player_object = Player(name, db)
    player = player_object.get_data()
    
    # The main menu (1st level loop)
    while True:
        header(f'Tervetuloa, {player["username"]}', player['balance'])
        
        main_menu = [
            'Tulostaulukot',
            'Oma pelihistoria',
            'Käyttäjäasetukset',
            'Poistu pelistä\n',
        ]
        
        if player.get('balance', 0) > 0 and not player.get('is_banned'):
            main_menu.insert(0, 'Pelivalikko') # allow the player to do other things, but play games.
        
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
                    header('Valitse peli', player['balance'])
                    
                    # 2nd level loop -> eg. game selection
                    for index, game in enumerate(game_menu, start=1):
                        print(f'{index})  {game}')
                            
                    game_choice = int(input(f'\nValitse peli (1 - {len(game_menu)}): '))
                    
                    match game_choice:
                        case 1: # dice
                            header('Nopanheitto', player['balance'])
                            
                            dice_game = Dice(player)
                            updated_player = dice_game.startGame() # returns the player object
                            
                            # TODO update the player db record accordingly
                        case 2: # back to main menu
                            break
                        case _:
                            print(f'Virheellinen valinta! Valitse numerolla {game_menu[0]} - {game_menu[-1]}')
                # ...
            case 5: # exit TODO dynamically get the last item
                print(f'\nNäkemiin, {player["username"]}!')
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