import curses
import asyncio
import time

class Controller:

    def __init__(self):
        self.loop = asyncio.new_event_loop()

    def test(self):
        t = Termianl_Information({'1':{'2':'NONE', '1':'NONE'}, '22':'VIEW'})
        t.display()
        t.exe()
        print(t.get_current_path_info())

class Termianl_Information:

    def __init__(self, path, screen = None):
        if screen == None:
            self.screen = curses.initscr()
        else:
            self.screen = screen
        curses.noecho()
        curses.cbreak()
        self.path : dict = path
        self.current_path : list = [str(x) for x in self.path.keys()]
        self.current_path : list = [self.current_path[0]]
        self.current_path_info : dict = self.get_current_path_info()
        self.current : str = str(self.current_path[0])
        self.current_index : int = 0
        self.current_max : int = len(self.get_current_path_info().keys()) - 1

    def setup(self):
        return curses.initscr()

    def setup_current(self):
        self.current = str([x for x in self.current_path_info][self.current_index])

    def get_current_path_info(self):
        path = self.path
        current = [x for x in self.current_path]
        del current[0]
        if not current == []:
            for x in current:
                path = path[x]
                path['BACK'] = 'BACK'
        else:
            path = self.path
        return path

    def move_UP(self):
        if not self.current_index == 0:
            self.current_index -= 1
            self.setup_current()
        self.display()

    def move_DOWN(self):
        if not self.current_index == self.current_max:
            self.current_index += 1
            self.setup_current()
        self.display()

    def next(self):
        self.current_path.append(self.current)
        self.current_index = 0
        self.current = str(self.current_path[0])
        self.current_path_info = self.get_current_path_info()
        self.current_max = len(self.current_path_info.keys()) - 1

    def back(self):
        del self.current_path[len(self.current_path)-1]
        self.current_path_info = self.get_current_path_info()
        self.current = self.current_path[len(self.current_path)-1]
        self.current_index = [x for x in self.current_path_info].index(self.current)
        self.current_max = len(self.current_path_info.keys()) - 1

    def use(self):
        value = self.current_path_info[self.current]
        if value == 'BACK':
            self.back()
        if isinstance(value, dict):
            self.next()
        self.display()

    def display(self):
        self.screen.clear()
        info = self.current_path_info
        self.screen.addstr(0, 0, 'TAB to exit')
        for x in range(len(info)):
            if x == self.current_index:
                space = ">> "
            else:
                space = "   "
            self.screen.addstr(x+2, 0, f'{space}{[b for b in info.keys()][x]}')

        self.screen.refresh()

    def exe(self):
        while True:
            self.display()
            c = self.screen.getch()
            if c == 9:
                break
            if c == 10:
                self.use()
            if c == ord('w') or c == ord('W'):
                self.move_UP()
            if c == ord('s') or c == ord('S'):
                self.move_DOWN()


def terminal_command(self):

    def do_func(func):
        self.commands[f"{func.__name__}"] = func
        return func

    return do_func

class Terminal_commands:

    def __init__(self, commands, screen = None):
        if screen == None:
            self.screen = curses.initscr()
        else:
            self.screen = screen
        self.history = []
        self.commands : dict = {}
        self.implement_commands(commands)
        self.setup_commands()
        self.screen = curses.initscr()
        curses.echo()
        curses.cbreak()
        self.screen.keypad(True)
        self.tracknum : int = 0


    def implement_commands(self, commands : dict):
        for x in commands:
            self.commands[f"i.{x}"] = commands[x]

    def dispaly(self):
        self.screen.clear()
        tracknum : int = 0
        for x in range(len(self.history)):
            self.screen.addstr(x, 0, self.history[x])
            tracknum = x
        self.screen.addstr(tracknum, 0, "")
        self.screen.addstr(tracknum + 1, 0, ">> ")
        self.tracknum = tracknum + 1
        self.screen.refresh()

    def run(self):
        # Initialisieren von curses
        stdscr = self.screen
        self.dispaly()
        # Hauptterminal-Schleife
        while True:
            self.dispaly()
            user_input = stdscr.getstr(self.tracknum, 3, 60)
            self.screen.refresh()
            user_input = user_input.decode("utf-8").split()
            if user_input:
                command = user_input[0]
                self.t_print(f'>  {command}')
                if command in self.commands:
                    output = self.commands[command]
                    if isinstance(output, str):
                        self.t_print(output)
                    else:
                        a = output(self)
                        curses.echo()
                        if a == 0:
                            break
                else:
                    self.t_print(f'Unbekannter Befehl "{command}"')

            # Warten auf Benutzereingabe

    def inputs(self, eingabe:dict):
        self.screen.clear()
        tracknum = 0
        for x in eingabe:
            if eingabe[x] == 'HIDDEN':
                curses.noecho()
            self.screen.addstr(tracknum, 0, f'{x}:')
            user_input = self.screen.getstr(tracknum, 1 + len(x), 60)
            self.screen.refresh()
            user_input = user_input.decode("utf-8").split()
            curses.echo()
            eingabe[x] = user_input[0]
            tracknum += 1
        return eingabe

    def t_print(self, info:str):
        self.history.append(info)
        self.dispaly()

    def setup_commands(self):

        @terminal_command(self)
        def clear(self):
            self.history = []
            self.dispaly()

        @terminal_command(self)
        def exit(self):
            return 0

        @terminal_command(self)
        def help(self):
            self.t_print('')
            self.t_print('Alle möglichen Befehle:')
            for x in self.commands:
                self.t_print(f'     {x}')
            self.t_print('')


def test(param):
    a = Termianl_Information({'1':{'2':'NONE', '1':'NONE'}, '22':'VIEW'}, param.screen)
    a.exe()

#c = Controller()
#c.test()
t = Terminal_commands({'a':'b', 't': test})
t.run()


