import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import storage

from math import round



def command(args, optargs, bl):
    i1 = main.parsearg(args[0], bl)
    o = round(i1)
    main.storeb(args[1], o, bl)