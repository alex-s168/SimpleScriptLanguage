import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import interpret as main

def datatypedefault(in_val: str, block_list: list):
    '''returns the default value of a string datatype'''
    match in_val:
        case "s":
            out = ""
        case "i":
            out = 0
        case "b":
            out = False
        case "a":
            out = [] 
        case "f":
            out = 0.0
        case _:
            main.errorprinter("Type" + in_val + " not found!", block_list)
    return out