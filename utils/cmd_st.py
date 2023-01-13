import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import storage
import tools



def command(args, optargs, bl):
    main.storeb(args[0], tools.datatypedefault(args[1]), bl)