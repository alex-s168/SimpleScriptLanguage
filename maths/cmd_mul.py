import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import storage



def command(args, optargs, bl):
    i1 = main.parsearg(args[0], bl)
    i2 = main.parsearg(args[1], bl)
    o = i1 * i2
    main.storeb(args[2], o, bl)