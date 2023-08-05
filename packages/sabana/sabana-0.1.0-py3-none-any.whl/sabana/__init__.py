__version__ = '0.1.0'

from termcolor import colored
from pyfiglet import Figlet 

def sabana():
    f = Figlet(font="banner3-D")
    print(colored(f.renderText("sabana"), "red"))

