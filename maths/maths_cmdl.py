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
from maths import cmd_asin
from maths import cmd_acos
from maths import cmd_atan
from maths import cmd_round
from maths import cmd_floor
from maths import cmd_ceil
from maths import cmd_fact
from maths import cmd_lim
from maths import cmd_sum
from maths import cmd_abs
from maths import cmd_sqrt
from maths import cmd_root
from maths import cmd_exp
from maths import cmd_loc
from maths import cmd_sign
from maths import cmd_pow

cmdl = []
cmdl.append(main.command("add", 3, 0, cmd_add.command))
cmdl.append(main.command("sub", 3, 0, cmd_sub.command))
cmdl.append(main.command("mul", 3, 0, cmd_mul.command))
cmdl.append(main.command("div", 3, 0, cmd_div.command))
cmdl.append(main.command("mod", 3, 0, cmd_mod.command))
cmdl.append(main.command("sin", 2, 0, cmd_sin.command))
cmdl.append(main.command("cos", 2, 0, cmd_cos.command))
cmdl.append(main.command("tan", 2, 0, cmd_tan.command))
cmdl.append(main.command("asin", 2, 0, cmd_asin.command))
cmdl.append(main.command("acos", 2, 0, cmd_acos.command))
cmdl.append(main.command("atan", 2, 0, cmd_atan.command))
cmdl.append(main.command("round", 2, 0, cmd_round.command))
cmdl.append(main.command("floor", 2, 0, cmd_floor.command))
cmdl.append(main.command("ceil", 2, 0, cmd_ceil.command))
cmdl.append(main.command("fact", 2, 0, cmd_fact.command))
cmdl.append(main.command("lim", 3, 0, cmd_lim.command))
cmdl.append(main.command("sum", 1, -1, cmd_sum.command))
cmdl.append(main.command("abs", 2, 0, cmd_abs.command))
cmdl.append(main.command("sqrt", 2, 0, cmd_sqrt.command))
cmdl.append(main.command("root", 3, 0, cmd_root.command))
cmdl.append(main.command("exp", 2, 0, cmd_exp.command))
cmdl.append(main.command("loc", 3, 0, cmd_loc.command))
cmdl.append(main.command("sign", 1, 0, cmd_sign.command))
cmdl.append(main.command("pow", 3, 0, cmd_sign.command))

def cmd(com: str, args: list, bl: list):
    for i in cmdl:
        if com.rstrip() == i.name:
            return [True, i.call(bl, args)]
    return [False, None]