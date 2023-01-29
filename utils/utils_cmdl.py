# import other stuff
import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import storage

# import commands

from utils import cmd_loop
from utils import cmd_conv
from utils import cmd_clv
from utils import cmd_st

cmdl = []

cmdl.append(main.command("loop", 2, 0, cmd_loop.command))
cmdl.append(main.command("conv", 3, 0, cmd_conv.command))
cmdl.append(main.command("clv", 1, 0, cmd_clv.command))
cmdl.append(main.command("st", 2, 0, cmd_st.command))


def cmd(com: str, args: list, bl: list):
    for i in cmdl:
        if com.rstrip() == i.name:
            return [True, i.call(bl, args)]
    return [False, None]