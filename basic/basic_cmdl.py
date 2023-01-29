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
from basic import cmd_vart
from basic import cmd_lcfb
from basic import cmd_sto
from basic import cmd_log
from basic import cmd_end
from basic import cmd_delay
from basic import cmd_gentemp
from basic import cmd_cinput

cmdl = []

cmdl.append(main.command("vart", 1, 1, cmd_vart.command))
cmdl.append(main.command("var", 1, 1, cmd_var.command))
cmdl.append(main.command("lcfb", 1, 0, cmd_lcfb.command))
cmdl.append(main.command("sto", 2, 0, cmd_sto.command))
cmdl.append(main.command("log", 1, 0, cmd_log.command))
cmdl.append(main.command("end", 0, 1, cmd_end.command))
cmdl.append(main.command("delay", 1, 0, cmd_delay.command))
cmdl.append(main.command("gentemp", 1, 1, cmd_gentemp.command))
cmdl.append(main.command("cinput", 1, 0, cmd_cinput.command))

def cmd(com: str, args: list, bl: list):
    for i in cmdl:
        if com.rstrip() == i.name:
            return [True, i.call(bl, args)]
    return [False, None]