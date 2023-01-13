import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import storage



def command(args, optargs, bl):
    o = 0
    for i in optargs:
        o += main.parsearg(i, bl)
    main.storeb(args[0], o, bl)