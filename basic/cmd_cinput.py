import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import storage
import time



def command(args, optargs, bl):
    x = time.time()
    main.storeb(args[0], input(), bl)
    storage.total_cinput_delay += time.time() - x