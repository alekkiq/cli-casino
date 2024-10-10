from abc import ABC, abstractmethod
from cli.common.utils import header, get_prompt, box_wrapper
import tabulate

class CLIView(ABC):
    def __init__(self, db_handler: object, player: object, view_name: str):
        self.db = db_handler
        self.player = player
        self.view_name = view_name.capitalize()
        
    @abstractmethod
    def view(self):
        '''
        This method should be implemented in the view class to handle the view-specific logic
        '''
        pass
    
    def show_header(self, hide_balance: bool = True, text: str = ''):
        '''
        Wrapper for the header cli helper function
        Has hide_balance as a default True.
        '''
        header(f'{self.view_name}{f'  |  {text}' if not text == '' else ''}', hide_balance = hide_balance)
    
    def validate_input(self, prompt: str, input_type: str, min_value: int = None, max_value: int = None, allowed_values: tuple = None, allow_empty: bool = False, sanitize: bool = False):
        '''
        Wrapper for the get_prompt cli helper function
        '''
        return get_prompt(prompt, input_type, min_value, max_value, allowed_values, allow_empty, sanitize)
    
    def sub_menu(self, options: list = [], isolate_last: bool = True) -> int:
        '''
        Creates & displays a sub-menu and returns the selected option
        '''
        while True:
            for index, option in enumerate(options, start = 1):
                if index == len(options) and isolate_last:
                    print(f'\n{index}. {option}\n')
                else:
                    print(f'{index}. {option}')
            
            return self.validate_input(f'\nValitse (1 - {len(options)}): ', 'int', 1, len(options))

    def display_table(self, data: list, headers: list, alignment: list, table_description: str = None):
        '''
        Displays a table with the given data, headers, and alignment
        '''
        if len(data) == 0:
            print('Ei näytettäviä tietoja.\n')
            return
        
        if alignment is None:
            alignment = ['center'] * len(headers)
            
        rows = [list(row) for row in data]
        
        table = tabulate.tabulate(
            rows, 
            headers, 
            tablefmt='fancy_grid', 
            colalign=alignment
        )
        
        print(f'{table}')
        
        if table_description:
            print(f'{table_description}\n')
    
    def run(self):
        while True:
            self.show_header(self.view_name)
            
            view = self.view()   
                
            if not view:
                break