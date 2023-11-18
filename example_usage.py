import  terminal


class test_class:

    def __init__(self):
        self.yes = False

    def build(self, ter, args):
        self.yes = True

    def run(self, ter, args):
        if self.yes == True:
            ter.t_print('working')

    def display(self, term: terminal.Terminal_commands, args):
        display = {'list': {'1': '1', '2': '2', '3': '3'}, 'nolist': 'nolist'}
        ter_display = terminal.Termianl_Information(display, term.screen)
        ter_display.run()


wow = 'wow'

count = 0

def info():
    return {'a': {'a': None, 'b': None, 'c': None}, 'b': None, 'c': None, f'{count}': None}


def get_info(ter, args):
    new_info = info()
    ter_display = terminal.Termianl_Information(new_info, ter.screen)
    ter_display.run()




def help(ter, args):
    ter.t_print('help')


e1 = test_class()

def example1():

    terminal1 = terminal.Terminal_commands({}, display_info="Type 'help' to see all commands or type 'exit' to exit")
    terminal1.add_commands(wow=wow, help=help, build=e1.build, run=e1.run, display=e1.display)
    terminal1.add_commands(terminal=get_info)
    controller = terminal.Controller()
    controller.set_start(terminal1)
    controller.run()

example1()