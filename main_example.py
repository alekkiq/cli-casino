from config import config
from Database import Database
from Player import Player
from time import sleep

from cli.Leaderboard import Leaderboard
from cli.GameHistory import GameHistory
from cli.PlayerProfile import PlayerProfile

from Games.Dice import Dice
from Games.Roulette import Roulette

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
                if player.get_ban_status() == 1:
                    print('Sinulla on aktiivinen porttikielto, et pääse pelaamaan.\n')
                    sleep(3)
                    continue
                         
                # TODO leverage the game_types table on this   
                game_menu = (
                    'Nopanheitto',
                    'Ruletti\n',
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
                        case 2: # roulette
                            header('Ruletti', player.get_balance())

                            roulette_game = Roulette(player, db)
                            roulette_game.start_game()
                            break
                        case 3:
                            break
                        case _:
                            print(f'Virheellinen valinta! Valitse numerolla 1 - {len(game_menu)}')
                # ...
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