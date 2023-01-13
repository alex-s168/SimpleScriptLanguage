import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import storage



def command(args, optargs, bl):
    c = 0
    for i in storage.subroutine_params:
        try:
            main.storeb(optargs[c], i,bl)
        except: pass
        c += 1
    storage.subroutine_params = []