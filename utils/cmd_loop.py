import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import storage



def command(args, optargs, bl):
    l = main.parsearg(args[0], bl)
    c = 0
    for i in range(l):
        storage.subroutine_params = [c]
        main.decodeblock(args[1], bl)
        c += 1