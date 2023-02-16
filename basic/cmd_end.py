import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import storage



def command(args, optargs, bl):
    storage.todo_end = True
    try:
        optargs[0]
        storage.todo_end_msg = main.parsearg(optargs[0], bl)
    except: pass