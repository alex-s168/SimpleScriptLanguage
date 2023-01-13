import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import storage

from math import factorial



def command(args, optargs, bl):
    i1 = main.parsearg(args[0], bl)
    if i1 < 0:
        main.errorprinter("input is negative!", bl)
    else:
        try:
            int(i1)
        except:
            main.errorprinter("input is not an integer!", bl)
    o = factorial(i1)
    main.storeb(args[1], o, bl)