import curses
import asyncio
from abc import ABC
import abc
import time

#controller to controll and build the terminal
class Controller():

    def __init__(self):
        #creates the asyncio event loop
        self.build = {}

    def run(self):
        self.build['START'].run()

    def set_start(self, info):
        self.build['START'] = info



class base_terminal:


    def screen_setup(self, screen):
        self.running = False
        if screen == None:
            self.screen = curses.initscr()
        else:
            self.screen = screen

    def display(self):
        raise NotImplementedError("Please Implement the method display")

    def run(self):
        raise NotImplementedError("Please Implement run")

    def start(self):
        if not self.running:
            self.running = True

    def stop(self):
        if self.running:
            self.running = False

    def conv_func(self, func):
        result = str(func)
        if result == None:
            return False
        else:
            return result

    def conv_str(self, STR):
        return STR

#this is a terminal used to display simple information
class Termianl_Information(base_terminal):

    #inits the
    def __init__(self, path, screen = None):
        #inits the screen, can be given by the parent class and reuses the screen
        self.screen_setup(screen)
        #setting for the terminal
        curses.noecho()
        curses.cbreak()
        #this is the whole path for the display of information
        self.path : dict = path
        self.path['EXIT'] = 'EXIT'
        self.path_conv()
        #setups the current path, this is how the programm knows where in the path we are
        self.current_path : list = [str(x) for x in self.path.keys()]
        self.current_path : list = [self.current_path[0]]
        #this is just the path info for the current path(= where we currently are) is saved
        self.current_path_info : dict = self.get_current_path_info()
        #this is the current
        self.current : str = str(self.current_path[0])
        self.current_index : int = 0
        self.current_max : int = len(self.get_current_path_info().keys()) - 1

    def setup_current(self):
        self.current = str([x for x in self.current_path_info][self.current_index])

    def get_current_path_info(self, search_path = None):
        path = self.path
        if search_path == None:
            current = [x for x in self.current_path]
        else:
            current = [x for x in search_path]
        del current[0]
        if not current == []:
            for x in current:
                path = path[x]
                path['BACK'] = 'BACK'
        else:
            path = self.path
        return path

    def move(self, move_UP:bool):
        if move_UP and self.current_index != 0:
            self.current_index -= 1
        elif not move_UP and self.current_index != self.current_max:
            self.current_index += 1
        self.setup_current()
        self.display()

    #goes to the next in the path
    def next(self):
        self.current_path.append(self.current)
        self.current_index = 0
        self.current = str(self.current_path[0])
        self.current_path_info = self.get_current_path_info()
        self.current_max = len(self.current_path_info.keys()) - 1

    #goes back in the current path
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
        elif value == 'EXIT':
            return 0
        elif isinstance(value, dict):
            self.next()
        self.display()

    def path_conv(self):

        def costum_path_info(path_path):
            path = self.path
            print(path_path)
            for x in path_path:
                path = path[x]
            return path

        path_list = []
        for x in self.path.keys():
            path_list.append([x])
        del path_list[path_list.index(['EXIT'])]



        while True:


            if path_list == []:
                break

            current = path_list[0]

            current_info = costum_path_info(current)

            if isinstance(current_info, dict):
                for x in current_info.keys():
                    current_copy = [b for b in current]
                    current_copy.append(x)
                    path_list.append(current_copy)

            elif isinstance(current_info, list):
                new_info = dict()
                for x in current_info:
                    new_info[str(x)] = None

                self.add_path_info(current, new_info)

            elif callable(current_info):
                result = current_info()
                self.add_path_info(current, result)
                path_list.append(current)


            del path_list[0]

    def add_path_info(self, path, info):
        new_path = self.path
        last_char = path[len(path) - 1]
        del path[len(path) - 1]
        for x in path:
            new_path = new_path[x]
        new_path[last_char] = info


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

    def run(self):
        self.start()
        while True:
            self.display()
            c = self.screen.getch()
            if c == 9:
                break
            if c == 10:
                output = self.use()
                if output == 0:
                    break
            if c == ord('w') or c == ord('W'):
                self.move(True)
            if c == ord('s') or c == ord('S'):
                self.move(False)
        self.stop()


def terminal_command(self, *args):
    def do_func(func):
        self.commands[f"{func.__name__}"] = func
        return func

    return do_func

class Terminal_commands(base_terminal):

    def __init__(self, commands:dict ,  screen = None, display_info:str = ''):
        self.screen_setup(screen)
        self.history = []
        self.commands : dict = {}
        self.implement_commands(commands)
        self.setup_commands()
        self.screen = curses.initscr()
        curses.echo()
        curses.cbreak()
        self.screen.keypad(True)
        self.tracknum : int = 0
        self.display_info = display_info

    def add_commands(self, **kwargs):
        for x in kwargs:
            self.commands[f"i.{x}"] = kwargs[x]

    def __call__(self, *args, **kwargs):
        print(self)

    def implement_commands(self, commands : dict):
        for x in commands:
            self.commands[f"i.{x}"] = commands[x]

    def display(self, ignore_input:bool=False):
        self.screen.clear()
        tracknum : int = 0
        for x in range(len(self.history)):
            self.screen.addstr(x, 0, self.history[x])
            tracknum = x
        self.screen.addstr(tracknum, 0, "")
        if ignore_input == False:
            self.screen.addstr(tracknum + 1, 0, ">> ")
        else:
            self.screen.addstr(tracknum + 1, 0, "")
        self.tracknum = tracknum + 1
        self.screen.refresh()

    def run(self):
        if self.history == []:
            self.history.append(self.display_info)
        # Initialisieren von curses
        stdscr = self.screen
        self.display()
        # Hauptterminal-Schleife
        while True:
            self.display()
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
                        output = output(self, user_input[1:])
                        curses.echo()
                        if output == 0:
                            break
                else:
                    self.t_print(f'Unknown Command "{command}"')

            # Warten auf Benutzereingabe

    def yes_no_question(self, input:str=''):
        self.t_print(input)
        self.t_print('y[es] or n[o]')
        self.display(True)
        while True:
            key = self.screen.getch()
            if key == ord('y') or key == ord('Y'):
                return True
            if key == ord('n') or key == ord('N'):
                return False

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
        self.display()

    def setup_commands(self):

        @terminal_command(self)
        def clear(self:Terminal_commands, args):
            self.history = []
            self.display()

        @terminal_command(self)
        def exit(self:Terminal_commands, args):
            return 0

        @terminal_command(self)
        def help(self:Terminal_commands, args):
            self.t_print('')
            self.t_print('Alle möglichen Befehle:')
            for x in self.commands:
                self.t_print(f'     {x}')
            self.t_print('')

class No_func(Exception):

    pass

class use_func():

    def __init__(self):
        self.terminal = None
        self.args :list = []


    def run(self, terminal, args):
        self.terminal = terminal
        self.args = args
        self.func()

    def func(self):
        raise NotImplemented

class Builder:

    def __init__(self, path:dict={}):
        self.build = path

    def Return(self):
        return self.build




