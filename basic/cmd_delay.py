import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import storage
import time



def command(args, optargs, bl):
    total_delay += main.parsearg(args[0], bl) / 1000
    time.sleep(main.parsearg(args[0], bl) / 1000) 