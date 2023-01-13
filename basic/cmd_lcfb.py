import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import storage



def command(args, optargs, bl):
    a_filename = str(main.parsearg(args[0], bl))

    bc = main.blockconvert(a_filename)

    storage.blocks.extend(bc[0])
    storage.blocknames.extend(bc[1])