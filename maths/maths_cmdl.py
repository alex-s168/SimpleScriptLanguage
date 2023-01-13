# import other stuff
import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import storage

# import commands

from maths import cmd_add
from maths import cmd_sub
from maths import cmd_mul
from maths import cmd_div
from maths import cmd_mod
from maths import cmd_sin
from maths import cmd_cos
from maths import cmd_tan
from maths import cmd_round
from maths import cmd_floor
from maths import cmd_ceil
from maths import cmd_fact
from maths import cmd_lim
from maths import cmd_sum

cmdl = []
cmdl.append(main.command("add", 3, 0, cmd_add.command))
cmdl.append(main.command("sub", 3, 0, cmd_sub.command))
cmdl.append(main.command("mul", 3, 0, cmd_mul.command))
cmdl.append(main.command("div", 3, 0, cmd_div.command))
cmdl.append(main.command("mod", 3, 0, cmd_mod.command))
cmdl.append(main.command("sin", 2, 0, cmd_sin.command))
cmdl.append(main.command("cos", 2, 0, cmd_cos.command))
cmdl.append(main.command("tan", 2, 0, cmd_tan.command))
cmdl.append(main.command("round", 2, 0, cmd_round.command))
cmdl.append(main.command("floor", 2, 0, cmd_floor.command))
cmdl.append(main.command("ceil", 2, 0, cmd_ceil.command))
cmdl.append(main.command("fact", 2, 0, cmd_fact.command))
cmdl.append(main.command("lim", 3, 0, cmd_lim.command))
cmdl.append(main.command("sum", 1, -1, cmd_sum.command))
cmdl.append(main.command("abs", 2, 0, cmd_abs.command))

def cmd(com: str, args: list, bl: list):
    for i in cmdl:
        if com.rstrip() == i.name:
            i.call(bl, args)
            return True