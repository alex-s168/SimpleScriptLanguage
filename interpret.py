import time
import sys
import math

if __name__ == "__main__":
    import basic.basic_cmdl as basic_cmdl
    import arrays.arrays_cmdl as array_cmdl
    import blocks.blocks_cmdl as blocks_cmdl
    import maths.maths_cmdl as math_cmdl
    import strings.strings_cmdl as strings_cmdl
    import utils.utils_cmdl as utils_cmdl

import storage

if __name__ == "__main__":
    time_total_start = time.time()

    for i in range(storage.tempvaramount):
        storage.varlist.append("tmp"+str(i))
        storage.varlistv.append(None)

def errorprinter(error, bl):
    print("\nERROR: "+error)
    print("Stacktrace:")
    for i in bl[1:]:
        print("Block:",i[0],i[1])
    sys.exit()

def store(where, val,bl):
    if where == "vtemp":
        vartemp = parsearg(val,bl)
    elif where[0] == "v":
        if where[1:] in storage.varlist:
            storage.varlistv[storage.varlist.index(where[1:])] = parsearg(val,bl)
        else:
            errorprinter("Variable " + where[1:] + " needs to be declared before it can be used!",bl)
    elif where == "_pass":
        pass
    else:
        errorprinter("No storage named "+where+"!",bl)

def storeb(where, val,bl):
    if where == "vtemp":
        storage.vartemp = val
    elif where[0] == "v":
        if where[1:] in storage.varlist:
            storage.varlistv[storage.varlist.index(where[1:])] = val
        else:
            errorprinter("Variable " + where[1:] + " needs to be declared before it can be used!",bl)
    elif where == "_pass":
        pass
    else:
        errorprinter("No storage named ",where , "!",bl)

def arrize(r,bl):
    x = r.split(",")
    n =  []
    for i in x:
        n.append(parsearg(i))
    return n

def arrizeb(r,bl):
    x = r.split(",")
    n =  []
    for i in x:
        n.append(i)
    return n

def parsearg(arg,bl):
    b = arg[0]
    r = arg[1:]

    if arg == "_space":
        return " "
    if arg == "_pi":
        return math.pi
    if arg == "_e":
        return math.exp(1)
    
    if arg == "vtemp":
        return storage.vartemp
    if b == "v":
        if r in storage.varlist:
            return storage.varlistv[storage.varlist.index(r)]
        else:
            errorprinter("Variable " + r + " not declared!",bl)
    if b == "s":
        return str(r)
    if b == "i":
        return int(r)
    if b == "f":
        return float(r)
    if b == "b":
        return bool(r)
    if b == "a":
        return arrize(r)
    errorprinter("Datatype " + b + " does not exist!",bl)
    sys.exit(-1)

def getindexname(arr2, search):
    x = 0
    o = None
    for i in arr2:
        if i == search:
            o = x
            break
        x += 1
    return o

class command:
    def __init__(self, _name: str, _args: int, _optargs: int, _func):
        self.name = _name
        self.args = _args
        self.optargs = _optargs
        self.func = _func

    def call(self, bl: str, arglist: list):
        if len(arglist) < self.args:
            errorprinter("missing arguments! Needs: "+str(self.args)+" Provided: "+str(len(arglist)), bl)
        if (len(arglist) > self.optargs + self.args) and not self.optargs == -1:
            errorprinter("too much arguments arguments!", bl)
        
        if self.optargs == -1:
            x = self.func(arglist[:self.args], arglist[self.args:], bl)
        else:
            x = self.func(arglist[:self.args], arglist[self.optargs:], bl)
        return x

def blockconvert(file):
    bl = []
    bn = []

    bl.append([])
    bn.append("__main__")

    print("\nBLOCKIFIER: Starting block conversion of file: "+file)

    with open(file) as file_in:
        curr_block = "__main__"
        for line in file_in:
            if line.startswith(":"):
                xc = ((line+"#").split("#")[0]).rstrip().lstrip()
                bl.append([])
                bn.append(str(xc[1:]))
                curr_block = xc[1:]
            else: 
                xc = (line+"#").split("#")[0]
                bl[getindexname(bn, curr_block)].append(xc.split(" "))
    
    print("BLOCKIFIER: Block conversion finished!\nBLOCKIFIER: Added",len(bl),"blocks!\n")

    return [bl, bn]

if __name__ == "__main__":
    time_dec_start = time.time()
    t = blockconvert(storage.file)
    storage.blocks = t[0]
    storage.blocknames = t[1]
    time_dec_end = time.time()

def insext(list: list, list2: list, pos: int):
    l = list

    c = pos
    for i in list2:
        l.insert(c, i)
        c+= 1

    return l

def getblock(name):
    try:
        return storage.blocks[getindexname(storage.blocknames, str(name))]
    except:
        print("ERROR: Block",name, "not found!")
        sys.exit(-1)

def main_cmd_cmd(com: str, args: list, bl: list):
    def cmd_iter(args, optargs, bl):
        l = parsearg(args[0],bl)
        c = 0
        for i in l:
            storage.subroutine_params = [c, i]
            decodeblock(args[1],bl)
            c += 1
    def cmd_jmp(args, optargs, bl):
        decodeblock(args[0], bl)

    cmdl = []

    cmdl.append(command("iter", 2, 0, cmd_iter))
    cmdl.append(command("jmp", 1, 0, cmd_jmp))

    for i in cmdl:
        if com.rstrip() == i.name:
            return [True, i.call(bl, args)]
    return [False, None]

def isnone(i):
    try:
        if i == None:
            return True
        return False
    except:
        return False

def decodeblock(name, _bl):
    bl = _bl

    contdec = True
    line = 0

    while contdec:
        if False:
            pass
        else:
            try:
                com = getblock(name)[line]
            except:
                print("\nPROGRAMM STOPPED! IT IS RECOMMENDED TO USE THE end COMMAND ON THE END OF THE PROGRAMM!")
                sys.exit(-1)
            if bl[0][0] == name:
                bl=[["__main__",""]]

            bl.append([str(name), "File: "+storage.file+"  Line: "+str(line+1)+" Command: "+com[0].rstrip()])
            x = 0
            for i in com:
                com[x] = i.rstrip()
                x += 1

            e = False

            tc = basic_cmdl.cmd(com[0], com[1:], bl)
            if not isnone(tc[1]): return x
            if tc[0]: e = True

            tc = blocks_cmdl.cmd(com[0], com[1:], bl)
            if not isnone(tc[1]): return x
            if tc[0]: e = True

            tc = array_cmdl.cmd(com[0], com[1:], bl)
            if not isnone(tc[1]): return x
            if tc[0]: e = True

            tc = strings_cmdl.cmd(com[0], com[1:], bl)
            if not isnone(tc[1]): return x
            if tc[0]: e = True

            tc = math_cmdl.cmd(com[0], com[1:], bl)
            if not isnone(tc[1]): return x
            if tc[0]: e = True

            tc = utils_cmdl.cmd(com[0], com[1:], bl)
            if not isnone(tc[1]): return x
            if tc[0]: e = True

            tc = main_cmd_cmd(com[0], com[1:], bl)
            if not isnone(tc[1]): return x
            if tc[0]: e = True
            
                
            # Uncomment later
            #if e == False:
            #   errorprinter("Command not found!", bl)


            match com[0]:

                case "scmb":                                        # Combines multiple strings                                                                                     scmb [out] [in1: s] [in2: s] ?[in3: s] ....
                    if not len(com)-1 <= 3:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    s = ""
                    for i in com[2:]:
                        try:
                            s = s + parsearg(i,bl)
                        except:
                            print("ERROR: Can only combine strings!",bl)
                            sys.exit(-1)
                    storeb(com[1], s,bl)

                case "aapp":                                         # Appends a value to a array                                                                                   aap [in] [element] [out]
                    if not len(com)-1 == 3:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    il  = parsearg(com[1],bl)
                    ie  = parsearg(com[2],bl)
                    nl = il

                    nl.append(ie)

                    storeb(com[3], nl,bl)

                case "spaceify":                                     # replaces all X with spaces of an string                                                                      spaceify [in] [what] [out]
                    if not len(com)-1 == 3:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    o = parsearg(com[1],bl).replace(parsearg(com[2],bl), " ")
                    storeb(com[3], o, bl)

                case "sarrify":                                      # converst string to a char-array                                                                              sarrify [in] [out]
                    if not len(com)-1 == 2:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    
                    storeb(com[2], [*parsearg(com[1],bl)], bl)

                case "aget":                                         # gets a value of an array                                                                                     aget [in] [pos] [out]
                    if not len(com)-1 == 3:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    il  = parsearg(com[1],bl)
                    ip  = parsearg(com[2],bl)
                    
                    o = il[ip]

                    storeb(com[3], o,bl)

                case "aset":                                         # sets a value of an array                                                                                     aset [in] [pos] [val] [out]
                    if not len(com)-1 == 4:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    il  = parsearg(com[1],bl)
                    ip  = parsearg(com[2],bl)
                    iv = parsearg(com[3],bl)

                    il[ip] = iv

                    storeb(com[4], il,bl)

                case "alen":                                         # gets the length of an array                                                                                  alen [in] [out]
                    if not len(com)-1 == 2:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    il  = parsearg(com[1],bl)

                    o = len(il)

                    storeb(com[2], o,bl)

                case "aext":                                         # extends a array with another array                                                                           aext [in] [in2] [out]
                    if not len(com)-1 == 3:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    il  = parsearg(com[1],bl)
                    ie  = parsearg(com[2],bl)
                    nl = il

                    nl.extend(ie)

                    storeb(com[3], nl,bl)

                case "asplit":                                       # splits a string and returns a array                                                                          asplit [in] [at] [out]
                    if not len(com)-1 == 3:
                        print("ERROR: missing arguments / too much arguments!",bl)
                    i1  = parsearg(com[1],bl)
                    i2  = parsearg(com[2],bl)
                    nl = i1.split(i2) 

                    storeb(com[3], nl,bl)
                        
                case "repl":                                           # replaces a element (string) in a string                                                                    repl [what] [with] [string] [out]
                    if not len(com)-1 == 4:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    s = parsearg(com[3],bl)
                    o = s.replace(parsearg(com[1],bl), parsearg(com[2],bl))
                    storeb(com[4], o,bl)

                case _:
                    pass

            line += 1 

time_run_start = time.time()

if __name__ == "__main__":
    decodeblock("__main__",[["__main__",""]])

    time_run_end = time.time()
    time_total_end = time.time()

    import os, psutil; used_mem = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2 * 1.049

    print("\nProgramm Finished!\n")
    print("dev data:")
    print("runtime: PYTHON-3-STANDARD-INTERPRETER")
    print("version: alpha.0.11 (13.01.2023)")
    print("total variables:",len(storage.varlist))
    print("- user variables:",len(storage.varlist)-storage.tempvaramount)
    print("- temp variables:",storage.tempvaramount)
    print("total blocks:",len(storage.blocks)+len(storage.imported_blocks))
    print("- local blocks:",len(storage.blocks))
    print("- imported blocks:",len(storage.imported_blocks))
    print("total time:",(time_total_end-time_total_start)* 1000,"ms")
    print("- decode time:",(time_dec_end-time_dec_start)* 1000,"ms")
    print("- run time:",(time_run_end-time_run_start)* 1000,"ms")
    print("- - run time (no delay):",(time_run_end-time_run_start-storage.total_delay)* 1000,"ms (might be unaccurate when delay is used)")
    print("- - run time (no delay + no cinput):",(time_run_end-time_run_start-storage.total_delay-storage.total_cinput_delay)* 1000,"ms (might be unaccurate when cinput or delay is used)")
    print("used memory:",used_mem,"MB")
    print("- main:",storage.get_var_size()*0.000001,"MB")
    print("- runtime:",14,"MB (inaccurate)")
    print("- interpreter:",used_mem-14,"MB (inaccurate)")
