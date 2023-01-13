import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import storage



def command(args, optargs, bl):
    storage.varlist.append(main.parsearg(args[0], bl))
    storage.varlistv.append("")

    if len(optargs) > 0:
        main.store("v"+args[0], optargs[0], bl)