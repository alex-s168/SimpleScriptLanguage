import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main

def datatypedefault(inp: str, bl: list):
    match inp:
            case "s": 
                o = ""
            case "i":
                o = 0
            case "b":
                o = False
            case "a":
                o = [] 
            case "f":
                o = 0.0
            case _:
                main.errorprinter("Type",inp, "not found!",bl)
    return o