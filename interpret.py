import time
import sys
import math

import basic.basic_cmdl as basic_cmdl
import arrays.arrays_cmdl as array_cmdl
import blocks.blocks_cmdl as blocks_cmdl
import maths.maths_cmdl as math_cmdl
import strings.strings_cmdl as strings_cmdl
import utils.utils_cmdl as utils_cmdl

import storage

time_total_start = time.time()

for i in range(storage.tempvaramount):
    storage.varlist.append("tmp"+str(i))
    storage.varlistv.append(None)

def errorprinter(error, bl):
    print("ERROR: "+error)
    print(bl[0])
    print("Stacktrace:")
    for i in bl[1]:
        print(i)

def store(where, val,bl):
    if where == "vtemp":
        vartemp = parsearg(val,bl)
    elif where[0] == "v":
        if where[1:] in storage.varlist:
            storage.varlistv[storage.varlist.index(where[1:])] = parsearg(val,bl)
        else:
            errorprinter("Variable " + where[1:] + " needs to be declared before it can be used!",bl)
            sys.exit(-1)
    elif where == "_pass":
        pass
    else:
        errorprinter("No storage named "+where+"!",bl)
        sys.exit(-1)

def storeb(where, val,bl):
    if where == "vtemp":
        vartemp = val
    elif where[0] == "v":
        if where[1:] in storage.varlist:
            storage.varlistv[storage.varlist.index(where[1:])] = val
        else:
            errorprinter("Variable " + where[1:] + " needs to be declared before it can be used!",bl)
            sys.exit(-1)
    elif where == "_pass":
        pass
    else:
        errorprinter("No storage named ",where , "!",bl)
        sys.exit(-1)

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
    global varlist
    global varlistv

    b = arg[0]
    r = arg[1:]

    if arg == "_space":
        return " "
    if arg == "vtemp":
        return storage.vartemp
    if b == "v":
        if r in storage.varlist:
            return storage.varlistv[storage.varlist.index(r)]
        else:
            errorprinter("Variable " + r + " not declared!",bl)
            sys.exit(-1)
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
            errorprinter("missing arguments!", bl)
        if len(arglist) > self.optargs + self.args:
            errorprinter("too much arguments arguments!", bl)
        
        self.func(arglist[:self.args], arglist[self.optargs:], bl)

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
    blocks = t[0]
    blocknames = t[1]
    time_dec_end = time.time()

def insext(list: list, list2: list, pos: int):
    l = list

    c = pos
    for i in list2:
        l.insert(c, i)
        c+= 1

    return l

def getblock(name):
    global blocknames
    global blocks

    try:
        return blocks[getindexname(blocknames, str(name))]
    except:
        print("ERROR: Block",name, "not found!")
        sys.exit(-1)

def decodeblock(name):
    global total_cinput_delay
    global subroutine_params
    global varlist
    global varlistv
    global total_delay
    global tempvaramount
    global blocks
    global imported_blocks
    global blocknames

    contdec = True
    line = 0

    while contdec:
        # todo!
        if False:
            pass
        else:
            com = getblock(name)[line]
            bl = "File: "+storage.file+" Block: "+str(name)+" Line: "+str(line+1)+" Command: "+com[0].rstrip()

            x = 0
            for i in com:
                com[x] = i.rstrip()
                x += 1

            e = False
            if basic_cmdl.cmd(com[0], com[1:], bl):
                e = True
            if blocks_cmdl.cmd(com[0], com[1:], bl):
                e = True
            if array_cmdl.cmd(com[0], com[1:], bl):
                e = True
            if strings_cmdl.cmd(com[0], com[1:], bl):
                e = True
            if math_cmdl.cmd(com[0], com[1:], bl):
                e = True
            if utils_cmdl.cmd(com[0], com[1:], bl):
                e = True
            
                
            # Uncomment later
            #if e == False:
            #   errorprinter("Command not found!", bl)




            match com[0]:

                case "lcfb":                                        # load code file blocks                                                                                         lcfb [filename]
                    if len(com)-1 > 1 or len(com)-1 < 1:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    a_filename = str(com[1])

                    bc = blockconvert(a_filename)

                    blocks.extend(bc[0])
                    blocknames.extend(bc[1])

                case "sto":                                         # stores something                                                                                              sto [what] [where]
                    if not len(com)-1 == 2:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    store(com[2], com[1],bl)

                case "log":                                         # log to console                                                                                                log [val]
                    if not len(com)-1 == 1:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    print("LOG: ", parsearg(com[1],bl))
                
                case "end":                                         # ends the script                                                                                               end
                    if not len(com)-1 < 1:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    contdec = False
                    return

                case "jmp":                                         # jumps to a code block and ends decoding of this block                                                         jmp [block]
                    if not len(com)-1 == 1:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    contdec = False
                    decodeblock(com[1])
                
                case "jsr":                                         # jumps to a codeblock but continues decoding after the codeblock is finished and stores the ret value          jsr [block] ?[out]
                    if not len(com)-1 <= 1:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    t = decodeblock(com[1])
                    try:
                        if any(c.isalpha() for c in com[2]):
                            store(com[2], t,bl)
                    except: pass
                    else:
                        store("vtemp", t,bl)
                
                case "jvsr":                                        # like jsr but also sends args to subroutine                                                                    jvsr [block] [out] [val1] ?[val2] ?[val3] ....
                    if not len(com)-1 <= 3:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    t = decodeblock(com[1])
                    store(com[2], t,bl)
                    subroutine_params = []
                    for i in com[2:]:
                        if any(c.isalpha() for c in com[2]):
                            subroutine_params.append(parsearg(i,bl))
                case "ret":                                         # returns a value when block is called from subroutine (to the subroutine command) also stops exec of block     ret ?[val]
                    if len(com)-1 > 1:
                        print("ERROR: too much arguments!",bl)
                        sys.exit(-1)
                    contdec = False
                    try:
                        if any(c.isalpha() for c in com[1]):
                            return com[1]
                    except:pass
                    return

                case "grv":                                         # gets subroutine values (when subroutine is called via a value-subroutine command)                             grv [out1] ?[out2] ?[out3] ?[out4] ....
                    c = 0
                    for i in subroutine_params:
                        try:
                            storeb(com[1+c], i,bl)
                        except: pass
                        c += 1
                    subroutine_params = []

                case "iter":                                        # iterates over a given list. calls a subroutine with two args: [id] [elem]                                     iter [arr] [block]
                    if not len(com)-1 == 2:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    l = parsearg(com[1],bl)
                    c = 0
                    for i in l:
                        subroutine_params = [c, i]
                        decodeblock(com[2])
                        c += 1

                case "loop":                                        # loops X times. calls a subroutine with one arg: [iteration]                                                   loop [amount] [block]
                    if not len(com)-1 == 2:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    l = parsearg(com[1],bl)
                    c = 0
                    for i in range(l):
                        subroutine_params = [c]
                        decodeblock(com[2])
                        c += 1

                case "scmb":                                        # Combines multiple strings                                                                                     scmb [out] [in1: s] [in2: s] ?[in3: s] ....
                    if not len(com)-1 <= 3:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    s = ""
                    for i in com[2:]:
                        try:
                            s = s + parsearg(i)
                        except:
                            print("ERROR: Can only combine strings!",bl)
                            sys.exit(-1)
                    storeb(com[1], s,bl)

                case "conv":                                        # Converts a value                                                                                              conv [in] [type] [out]
                    if not len(com)-1 == 3:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    i = parsearg(com[1],bl)
                    o = None

                    match com[2]:
                        case "s":
                            o = str(i)
                        case "i":
                            o = int(i)
                        case "b":
                            o = bool(i)
                        case "a":
                            o = arrizeb(i,bl)
                        case "f":
                            o = float(i)
                        case _:
                            print("ERROR: Type ",com[2], " not found!",bl)
                            sys.exit(-1)
                    
                    storeb(com[3], o,bl)

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
                case "clv":                                          # Clears a value (sets to none)                                                                                clv [out]
                    if not len(com)-1 == 1:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    storeb(com[1], None,bl)

                case "add":                                          # do simple math stuff (add)                                                                                   add [in1] [in2] [out]
                    if not len(com)-1 == 3:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    i1 = parsearg(com[1],bl)
                    i2 = parsearg(com[2],bl)

                    o = i1 + i2

                    storeb(com[3], o,bl)
                
                case "sub":                                          # do simple math stuff (sub)                                                                                   sub [in1] [in2] [out]
                    if not len(com)-1 == 3:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    i1 = parsearg(com[1],bl)
                    i2 = parsearg(com[2],bl)
                    o = i1 - i2

                    storeb(com[3], o,bl)

                case "mul":                                          # do simple math stuff (mul)                                                                                   mul [in1] [in2] [out]
                    if not len(com)-1 == 3:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    i1 = parsearg(com[1],bl)
                    i2 = parsearg(com[2],bl)
                    o = i1 * i2

                    storeb(com[3], o,bl)

                case "div":                                          # do simple math stuff (div)                                                                                   div [in1] [in2] [out]
                    if not len(com)-1 == 3:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    i1 = parsearg(com[1],bl)
                    i2 = parsearg(com[2],bl)
                    o = i1 / i2

                    storeb(com[3], o,bl)
                    
                case "mod":                                          # do simple math stuff (mod)                                                                                   mod [in1] [in2] [out]
                    if not len(com)-1 == 3:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    i1 = parsearg(com[1],bl)
                    i2 = parsearg(com[2],bl)
                    o = i1 % i2

                    storeb(com[3], o,bl)
                    
                case "sin":                                          # do simple math stuff (sin)                                                                                   sin [in1] [out]
                    if not len(com)-1 == 2:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    i1 = parsearg(com[1],bl)
                    o = math.sin(i1)

                    storeb(com[2], o,bl)
                    
                case "cos":                                          # do simple math stuff (cos)                                                                                   cos [in1] [out]
                    if not len(com)-1 == 2:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    i1 = parsearg(com[1],bl)
                    o = math.cos(i1)

                    storeb(com[2], o,bl)
                    
                case "tan":                                          # do simple math stuff (tan)                                                                                   tan [in1] [out]
                    if not len(com)-1 == 2:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    i1 = parsearg(com[1],bl)
                    o = math.tan(i1)

                    storeb(com[2], o,bl)

                case "st":                                           # set type of variable                                                                                         st [out] [type]
                    if not len(com)-1 == 2:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    o = None
                    match com[2]:
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
                            print("ERROR: Type ",com[2], " not found!",bl)
                            sys.exit(-1)
                    storeb(com[1], o,bl)
                
                case "delay":                                        # waits for X seconds, then continues                                                                          delay [ms]
                    if not len(com)-1 == 1:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    total_delay += parsearg(com[1],bl)/1000
                    time.sleep(parsearg(com[1],bl)/1000) 
                
                case "gentemp":                                      # generates temp variables                                                                                     gentemp [amount] ?[type]
                    if not len(com)-1 <= 2:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    if any(c.isalpha() for c in com[2]):
                        o = None
                        match com[2]:
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
                                print("ERROR: Type ",com[2], " not found!",bl)
                                sys.exit(-1)
                        for i in range(parsearg(com[1],bl )):
                            storage.varlist.append("tmp"+str(i+storage.tempvaramount))
                            storage.varlistv.append(None)
                            storeb("vtmp"+str(i+storage.tempvaramount), o,bl)
                        storage.tempvaramount += parsearg(com[1],bl)
                            
                    else:
                        for i in range(parsearg(com[1],bl)):
                            storage.varlist.append("tmp"+str(i+storage.tempvaramount))
                            storage.varlistv.append(None)
                        
                case "repl":                                           # replaces a element (string) in a string                                                                    repl [what] [with] [string] [out]
                    if not len(com)-1 == 4:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    s = parsearg(com[3],bl)
                    o = s.replace(parsearg(com[1],bl), parsearg(com[2],bl))
                    storeb(com[4], o,bl)

                case "eq":                                             # Jumps to a block if both inputs are equal                                                                  eq [block] [in1] [in2]
                    if not len(com)-1 == 3:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    if parsearg(com[2],bl) == parsearg(com[3],bl):
                        contdec = False
                        decodeblock(com[1])

                case "neq":                                            # Jumps to a block if both inputs are not equal                                                              neq [block] [in1] [in2]
                    if not len(com)-1 == 3:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    if not parsearg(com[2],bl) == parsearg(com[3],bl):
                        contdec = False
                        decodeblock(com[1])
                
                case "seq":                                             # Jumps to a subroutine if both inputs are equal                                                            seq [block] [in1] [in2] ?[out]
                    if not len(com)-1 <= 3:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    if parsearg(com[2],bl) == parsearg(com[3],bl):
                        t = decodeblock(com[1])
                        try:
                            if any(c.isalpha() for c in com[4]):
                                store(com[4], t,bl)
                            else:
                                store("vtemp", t,bl)
                        except:
                            store("vtemp", t,bl)

                case "sneq":                                            # Jumps to a subroutine if both inputs are not equal                                                        sneq [block] [in1] [in2] ?[out]
                    if not len(com)-1 <= 3:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    if not parsearg(com[2],bl) == parsearg(com[3],bl):
                        t = decodeblock(com[1])
                        try:
                            if any(c.isalpha() for c in com[4]):
                                store(com[4], t,bl)
                            else:
                                store("vtemp", t,bl)
                        except:
                            store("vtemp", t,bl)

                case "cinput":                                          # gets input from console                                                                                   cinput [out]
                    if not len(com)-1 == 1:
                        print("ERROR: missing arguments / too much arguments!",bl)
                        sys.exit(-1)
                    x = time.time()
                    storeb(com[1],input(),bl)
                    total_cinput_delay += time.time() - x

                case _:
                    pass
                    #outdated
                    #if any(c.isalpha() for c in com[0]):
                    #    print("ERROR: command not found!",bl)
                    #    sys.exit(-1)

            line += 1

time_run_start = time.time()

if __name__ == "__main__":
    decodeblock("__main__")

time_run_end = time.time()
time_total_end = time.time()

import os, psutil; used_mem = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2 * 1.049

if __name__ == "__main__":
    print("\nProgramm Finished!\n")
    print("dev data:")
    print("runtime: PYTHON-3-STANDARD-INTERPRETER")
    print("version: alpha.0.10 (12.01.2023)")
    print("total variables: ",len(storage.varlist))
    print("- user variables: ",len(storage.varlist)-storage.tempvaramount)
    print("- temp variables: ",storage.tempvaramount)
    print("total blocks: ",len(blocks)+len(storage.imported_blocks))
    print("- local blocks: ",len(blocks))
    print("- imported blocks: ",len(storage.imported_blocks))
    print("total time: ",(time_total_end-time_total_start)* 1000," ms")
    print("- decode time: ",(time_dec_end-time_dec_start)* 1000," ms")
    print("- run time: ",(time_run_end-time_run_start)* 1000," ms")
    print("- - run time (no delay): ",(time_run_end-time_run_start-storage.total_delay)* 1000," ms (might be unaccurate when delay is used)")
    print("- - run time (no delay + no cinput): ",(time_run_end-time_run_start-storage.total_delay-storage.total_cinput_delay)* 1000," ms (might be unaccurate when cinput or delay is used)")
    print("used memory: ",used_mem," MB")
    print("- runtime: ",14," MB (inaccurate)")
    print("- interpreter: ",used_mem-14," MB (inaccurate)")
