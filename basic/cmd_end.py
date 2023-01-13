import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import storage



def command(args, optargs, bl):
    try:
        optargs[0]
        sys.exit("Programm stopped! " + main.parsearg(optargs[0], bl))
    except:
        sys.exit("Programm stopped!")