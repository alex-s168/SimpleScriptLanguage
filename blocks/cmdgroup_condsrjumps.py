import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import storage



def eq_command(args, optargs, bl):
    if main.parsearg(args[1], bl) == main.parsearg(args[2], bl):
        t = main.decodeblock(args[0],bl)
        
        if len(optargs > 0):
            main.store(optargs[0], t,bl)

def neq_command(args, optargs, bl):
    if main.parsearg(args[1], bl) == main.parsearg(args[2], bl):
        t = main.decodeblock(args[0],bl)
        
        if len(optargs > 0):
            main.store(optargs[0], t,bl)