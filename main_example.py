import argparse
from time import sleep

from config import config
from Database import Database
from Player import Player

from cli.Leaderboard import Leaderboard
from cli.GameHistory import GameHistory
from cli.PlayerProfile import PlayerProfile

from Games.Dice import Dice
from Games.Roulette import Roulette
from Games.CoinFlip import CoinFlip
from Games.ventti import Ventti
from Games.Slots import Slots

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
            'Pelit\n',
            'Tulostaulukot',
            'Oma pelihistoria',
            'Profiili\n',
            'Poistu pelistä\n',
        ]
        
        for index, choice in enumerate(main_menu, start = 1):
            print(f'{index})  {choice}')
        
        choice = int(input(f'\nValitse (1 - {len(main_menu)}): '))
        
        match choice:
            case 1: # game selection
                # Should very well be its own function
                
                if player.get_ban_status() == 1:
                    print('Sinulla on aktiivinen porttikielto, et pääse pelaamaan.\n')
                    sleep(3)
                    continue
                         
                # get the game types from the d
                game_menu = get_game_menu(db)
                
                # Sub menu, eg. game selection (2nd level loop)
                while True:
                    header('Valitse peli', player.get_balance())
                    
                    # 2nd level loop -> eg. game selection
                    for index, (game_name, _) in enumerate(game_menu, start=1):
                        print(f'{index})  {game_name}')
                        
                        if index == len(game_menu) - 1:
                            print()
                    
                    game_choice = int(input(f'\nValitse peli (1 - {len(game_menu)}): '))
                    
                    if game_choice < 1 or game_choice > len(game_menu):
                        print(f'Virheellinen valinta! Valitse numerolla 1 - {len(game_menu)}')
                        continue
                    
                    selected_game = game_menu[game_choice - 1][1]
                    selected_game_name = game_menu[game_choice - 1][0]
                    
                    header(selected_game_name.capitalize(), player.get_balance())
                    
                    match selected_game:
                        case 'dice':
                            dice_game = Dice(player, db)
                            dice_game.start_game()
                        case 'roulette':
                            roulette_game = Roulette(player, db)
                            roulette_game.start_game()
                        case 'twentyone':
                            twenty_one_game = Ventti(player, db)
                            twenty_one_game.start_game()
                        case 'slots':
                            slots_game = Slots(player, db)
                            slots_game.start_game()
                        case 'coinflip':
                            coinflip_game = CoinFlip(player, db)
                            coinflip_game.start_game()
                        case 'back': # back to the main menu
                            break
                        case _:
                            print(f'Virheellinen valinta! Valitse numerolla 1 - {len(game_menu)}')
            case 2:
                header('Tulostaulukot', player.get_balance())
                
                leaderboard = Leaderboard(db)
                leaderboard.start_leaderboard()
            case 3:
                header('Oma pelihistoria', player.get_balance())
                
                game_history = GameHistory(db, player)
                game_history.start_game_history()
            case 4:
                header('Profiili', player.get_balance())
                
                player_profile = PlayerProfile(db, player)
                player_profile.start_player_profile()
            case _ if choice == len(main_menu):
                player.save() # save the player's data once more before exiting
                print(f'\nNäkemiin, {player.get_username()}!')
                break
            case _: # incorrect input
                print(f'Virheellinen valinta! Valitse numerolla {main_menu[0]} - {main_menu[-1]}')
    
# helpers
def get_game_menu(db) -> list:
    '''
    Gets the game types from the database and returns their names and classes as a list of tuples
    '''
    back_to_menu = ('Palaa päävalikkoon\n', 'back')
    try:
        result = db.query('''SELECT name, name_en FROM game_types''', cursor_settings = {'dictionary': True})
        
        if result['result_group']:
            game_types = [(game['name'].capitalize(), game['name_en']) for game in result['result']]
            game_types.append(back_to_menu)
            return game_types
        else:
            return [back_to_menu]
    except Exception as error:
        return [back_to_menu]
    
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

def setup_database():
    '''
    Sets up the database
    '''
    db_configs = config()
    db = Database(
        config = db_configs, 
        connect = True, 
        setup = True
    )
    db.connection.close()
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="CLI Casino")
    parser.add_argument('--setup', action='store_true', help='Start the casino with the setup for the database')
    args = parser.parse_args()
    
    if args.setup:
        print('Setting up the database...')
        
        if setup_database():
            print('Database setup complete')
        else:
            print('Database setup failed')
    else:
        main()