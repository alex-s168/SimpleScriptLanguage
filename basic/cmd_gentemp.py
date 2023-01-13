import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import tools
import storage



def command(args, optargs, bl):
    try:
        optargs[0]

        o = tools.datatypedefault(optargs[0])

        for i in range( main.parsearg(args[0], bl)):
            storage.varlist.append("tmp"+str(i+storage.tempvaramount))
            storage.varlistv.append(None)
            main.storeb("vtmp"+str(i+storage.tempvaramount), o, bl)
        storage.tempvaramount += main.parsearg(args[0],bl)
            
    except:
        for i in range(main.parsearg(args[0],bl)):
            storage.varlist.append("tmp"+str(i+storage.tempvaramount))
            storage.varlistv.append(None)