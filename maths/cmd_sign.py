import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import storage



def command(args, optargs, bl):
    i1 = main.parsearg(args[0], bl)
    if i1 > 0:
        o = 1
    elif i1 == 0:
        o = 0
    else:
        o = -1
    main.storeb(args[1], o, bl)