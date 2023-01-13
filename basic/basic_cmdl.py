# import other stuff
import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import storage

# import commands

from basic import cmd_var

cmdl = []

cmdl.append(main.command("var", 1, 1, cmd_var.command))

def cmd(com: str, args: list, bl: list):
    for i in cmdl:
        if com.rstrip() == i.name:
            i.call(bl, args)
            return True