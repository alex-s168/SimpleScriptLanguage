# import other stuff
import sys, os
import pathlib as path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main
import storage

# import commands

from blocks import cmd_jmp
from blocks import cmd_jsr
from blocks import cmd_jvsr
from blocks import cmd_ret
from blocks import cmd_grv
from blocks import cmdgroup_condjumps
from blocks import cmdgroup_condsrjumps

cmdl = []

cmdl.append(main.command("jmp", 1, 0, cmd_jmp.command))
cmdl.append(main.command("jsr", 1, 1, cmd_jsr.command))
cmdl.append(main.command("jvsr", 2, -1, cmd_jvsr.command))
cmdl.append(main.command("ret", 1, 0, cmd_ret.command))
cmdl.append(main.command("grv", 0, -1, cmd_grv.command))
cmdl.append(main.command("eq", 3, 0, cmdgroup_condjumps.eq_command))
cmdl.append(main.command("neq", 3, 0, cmdgroup_condjumps.neq_command))
cmdl.append(main.command("seq", 3, 1, cmdgroup_condsrjumps.eq_command))
cmdl.append(main.command("sneq", 3, 1, cmdgroup_condsrjumps.neq_command))

def cmd(com: str, args: list, bl: list):
    for i in cmdl:
        if com.rstrip() == i.name:
            i.call(bl, args)
            return True