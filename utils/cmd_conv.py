import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import storage



def command(args, optargs, bl):
    i = main.parsearg(args[0], bl)
    o = None

    match args[1]:
        case "s":
            o = str(i)
        case "i":
            o = int(i)
        case "b":
            o = bool(i)
        case "a":
            o = main.arrizeb(i, bl)
        case "f":
            o = float(i)
        case _:
            main.errorprinter("Type ", args[1], " not found!", bl)
    
    main.storeb(args[2], o, bl)