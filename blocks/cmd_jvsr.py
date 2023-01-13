import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import storage



def command(args, optargs, bl):
    t = main.decodeblock(args[0])
    main.store(args[1], t, bl)
    storage.subroutine_params = []

    for i in optargs:
        storage.subroutine_params.append(main.parsearg(i, bl))