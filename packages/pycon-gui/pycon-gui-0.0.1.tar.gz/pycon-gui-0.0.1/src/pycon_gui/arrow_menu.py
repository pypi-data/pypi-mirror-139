from platform import system
from rich.console import Console
from rich.style import Style
from rich.color import Color
import sys

OS_TYPE = system()
if   OS_TYPE == 'Windows':
    import msvcrt
elif OS_TYPE == 'Linux':
    from getch import getch

class ArrowMenuConfig:
    def __init__(self,
                 menu_color: Color = None,
                 active_menu_color: Color = None,
                 justify: str = 'center',
                 marker: str = '',
                 title: str = None,
                 description: str = None,
                 back_button: str = 'enter',
                 close_after_select: bool = False) -> None:
        
                    self.menu_color: Color = menu_color
                    self.active_menu_color: Color = active_menu_color
                    self.justify: str = justify
                    self.marker: str = marker
                    self.title: str = title
                    self.description: str = description
                    self.back_button: str = back_button
                    self.close_after_select: bool = close_after_select

class ArrowMenuPosition:
    def __init__(
        self,
        name: str,
        event
        ) -> None:
        self.id: int
        self.name: str = name
        self.event = event
        self.is_active: bool = False

class ArrowMenu:
    submenus = list()
    parent = None
    def __init__(self,
                 config: ArrowMenuConfig = None,
                 menu_color: Color = None,
                 active_menu_color: Color = None,
                 justify: str = 'center',
                 marker: str = '',
                 title: str = None,
                 description: str = None,
                 back_button: str = 'enter',
                 close_after_select: bool = False) -> None:
        
        if config != None:
            menu_color = config.menu_color
            active_menu_color = config.active_menu_color
            justify = config.justify
            marker = config.marker
            title = config.title
            description = config.description
            back_button = config.back_button
            close_after_select = config.close_after_select
        
        self.console: Console = Console()
        self.active_pos_id: int = 0
        self.menu_positions: list[ArrowMenuPosition] = list[ArrowMenuPosition]()

        if menu_color == None:
            self.menu_color = Style()
        elif type(menu_color) == str:
            self.menu_color = self.console.get_style(menu_color)
        else: self.menu_color = menu_color
        
        if active_menu_color == None:
            self.active_menu_color = Style(reverse=True)
        elif type(menu_color) == str:
            self.active_menu_color = self.console.get_style(active_menu_color)
        else: self.active_menu_color = active_menu_color
        self.justify = justify
        self.marker = marker
        self.title = title
        self.description = description
        self.back_button = back_button.strip().lower()
        self.close_after_select = close_after_select
        
        _handled_buttons = ['enter', 'spacebar', 'esc', 'up', 'down', 'left', 'right']
        
        if self.back_button not in _handled_buttons:
            self.back_button = 'enter'
            
    def read_key() -> str:
        if OS_TYPE == 'Windows':
            key: bytes = msvcrt.getch()
            if key in (b'\x00', b'\xe0'):
                key: bytes = msvcrt.getch()
                if   key == b'H': return 'up'
                elif key == b'P': return 'down'
                elif key == b'K': return 'left'
                elif key == b'M': return 'right'
            elif key == b'\x1b': return 'esc'
            elif key == b'\r'  : return 'enter'
            elif key == b' '   : return 'spacebar'
        elif OS_TYPE == 'Linux':
            key = getch()
            if key in ('\x1b'):
                getch() #skip '[' as 2'nd symbol
                key = getch()
                if   key == 'A': return 'up'
                elif key == 'B': return 'down'
                elif key == 'D': return 'left'
                elif key == 'C': return 'right'
            # elif key == b'\x1b': return 'esc'
            elif key == '\n'  : return 'enter'
            elif key == ' '   : return 'spacebar'
                
    def add_position(self, position: ArrowMenuPosition) -> None:
        position.id = len(self.menu_positions)
        self.menu_positions.append(position)

    def add_positions(self, positions: list[ArrowMenuPosition]) -> None:
        for position in positions:
            position.id = len(self.menu_positions)
            self.menu_positions.append(position)

    def compose(self, menu_structure: dict) -> None:
        for key in menu_structure:
            if isinstance(menu_structure[key], str) and menu_structure[key][0:2] == '..':
                self.add_position(ArrowMenuPosition(key, lambda: self.parent.open()))
                break
                
            if type(menu_structure[key]) == dict:
                submenu = ArrowMenu(menu_color = self.menu_color,
                                    active_menu_color = self.active_menu_color,
                                    justify = self.justify,
                                    marker  = self.marker)
                for sub_key in list(menu_structure[key]):
                    if isinstance(menu_structure[key][sub_key], ArrowMenuConfig):
                        submenu = ArrowMenu(menu_structure[key][sub_key])
                        del menu_structure[key][sub_key]
                submenu.parent = self
                self.submenus.append(submenu)
                submenu.compose(menu_structure[key])
                self.add_position(ArrowMenuPosition(key, submenu.open))
            else: self.add_position(ArrowMenuPosition(key, menu_structure[key]))

    def _str_gen(self, count: int, symbol: str = ' '):
        return  ''.join([symbol for num in range(count)])
                    
    def draw_position(self, position: ArrowMenuPosition) -> None:
        mp, mp_end, amp, amp_end = '','','',''
                
        if self.justify == 'left':
            mp      = self._str_gen(len(self.marker)) + position.name
            mp_end  = '\n'
            amp     = self.marker + position.name
            amp_end = '\n'
        elif self.justify == 'center':
            mp      =  position.name
            mp_end  = '\n'
            amp     = self.marker + position.name
            amp_end = self._str_gen(len(self.marker)) + '\n'
        elif self.justify == 'right':
            mp      =  position.name
            mp_end  = '\n'
            amp     = self.marker + position.name
            amp_end = '\n'
        
        if position.is_active: self.console.print(amp,
                                                  style = self.active_menu_color, 
                                                  highlight = False, 
                                                  justify = self.justify,
                                                  end = amp_end)
        else:                  self.console.print(mp,
                                                  style = self.menu_color, 
                                                  highlight = False, 
                                                  justify = self.justify,
                                                  end = mp_end)

    def draw_positions(self) -> None:
        self.console.clear()
        if self.description != None:
            self.console.print(self.description + '\n\n', 
                               style = self.menu_color, 
                               justify=self.justify)
        if self.title != None:
            self.console.print(self.title + '\n', 
                               style = self.menu_color, 
                               justify=self.justify)
            
        for position in self.menu_positions:
            if    position.id == self.active_pos_id: position.is_active = True
            else: position.is_active = False
            self.draw_position(position)

    def open(self) -> None:
        
        self.cont: bool = True
        self.draw_positions()

        while self.cont:
            menu_pos = ArrowMenu.read_key()
            if   menu_pos == 'up':
                if self.active_pos_id <= 0: self.active_pos_id = len(self.menu_positions) - 1
                else: self.active_pos_id -= 1
                self.draw_positions()
            elif menu_pos == 'down':
                if self.active_pos_id >= len(self.menu_positions) - 1: self.active_pos_id = 0
                else: self.active_pos_id += 1
                self.draw_positions()
            elif menu_pos == 'enter':
                if self.close_after_select: self.cont = False
                self.console.clear()
                self.menu_positions[self.active_pos_id].event()
                if not self.close_after_select:
                    back_btn = ArrowMenuPosition(f'BACK <{self.back_button}>', None)
                    back_btn.is_active = True
                    self.draw_position(back_btn)
                    while ArrowMenu.read_key() != self.back_button: pass
                    self.draw_positions()
            elif menu_pos == 'esc':
                sys.exit()
