import time
import sys

time_total_start = time.time()

blocks = []
varlist = []
varlistv = []
vartemp = None
subroutine_params = []
total_delay = 0

tempvaramount = 0
file = "test.ssl"

blocks.append([])

for i in range(tempvaramount):
    varlist.append("tmp"+str(i))
    varlistv.append(None)


def store(where, val):
    if where == "vtemp":
        vartemp = parsearg(val)
    elif where[0] == "v":
        if where[1:] in varlist:
            varlistv[varlist.index(where[1:])] = parsearg(val)
        else:
            print("ERROR: Variable " + where[1:] + " needs to be declared before it can be used!")
            sys.exit(-1)
    elif where == "_pass":
        pass
    else:
        print("ERROR: No storage named ",where , "!")
        sys.exit(-1)

def storeb(where, val):
    if where == "vtemp":
        vartemp = val
    elif where[0] == "v":
        if where[1:] in varlist:
            varlistv[varlist.index(where[1:])] = val
        else:
            print("ERROR: Variable " + where[1:] + " needs to be declared before it can be used!")
            sys.exit(-1)
    elif where == "_pass":
        pass
    else:
        print("ERROR: No storage named ",where , "!")
        sys.exit(-1)

def arrize(r):
    x = r.split(",")
    n =  []
    for i in x:
        n.append(parsearg(i))
    return n

def arrizeb(r):
    x = r.split(",")
    n =  []
    for i in x:
        n.append(i)
    return n

def parsearg(arg):
    global varlist
    global varlistv

    b = arg[0]
    r = arg[1:]

    if arg == "_space":
        return " "
    if arg == "vtemp":
        return vartemp
    if b == "v":
        if r in varlist:
            return varlistv[varlist.index(r)]
        else:
            print("ERROR: Variable " + r + " not declared!")
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
    print("ERROR: Datatype " + b + " does not exist!")
    sys.exit(-1)

time_dec_start = time.time()

print("\nStarting block conversion of file: "+file)

with open(file) as file_in:
    curr_block = 0
    for line in file_in:
        if line.startswith(":"):
            curr_block = int(line[1:])
            blocks.insert(curr_block, [])
        else: 
            blocks[curr_block].append(line.split(" "))

print("Block conversion finished!\n")
time_dec_end = time.time()

def decodeblock(id):
    global subroutine_params
    global varlist
    global varlistv
    global total_delay
    global tempvaramount

    id = int(id)

    if len(blocks)-1 < id:
        return

    contdec = True
    line = 0

    while contdec:
        if (line > len(blocks[id])-1) or (id > len(blocks)-1):
            contdec = False
            decodeblock(id+1)
            return
        else:
            com = blocks[id][line]

            x = 0
            for i in com:
                com[x] = i.rstrip()
                x += 1

            match com[0]:
                
                case "var":                                         # creates a variable                                                                                            var [name] ?[value]
                    varlist.append(com[1])
                    varlistv.append("")
                    try:
                        if any(c.isalpha() for c in com[2]):
                            store("v"+com[1], com[2])
                    except:
                        pass

                case "sto":                                         # stores something                                                                                              sto [what] [where]
                    store(com[2], com[1])

                case "log":                                         # log to console                                                                                                log [val]
                    print("LOG: ", parsearg(com[1]))
                
                case "end":                                         # ends the script                                                                                               end
                    contdec = False
                    return

                case "jmp":                                         # jumps to a code block and ends decoding of this block                                                         jmp [block]
                    contdec = False
                    decodeblock(com[1])
                
                case "jsr":                                         # jumps to a codeblock but continues decoding after the codeblock is finished and stores the ret value          jsr [block] ?[out]
                    t = decodeblock(com[1])
                    try:
                        if any(c.isalpha() for c in com[2]):
                            store(com[2], t)
                        else:
                            store("vtemp", t)
                    except:
                        store("vtemp", t)
                
                case "jvsr":                                        # like jsr but also sends args to subroutine                                                                    jvsr [block] [out] [val1] ?[val2] ?[val3] ....
                    t = decodeblock(com[1])
                    store(com[2], t)
                    subroutine_params = []
                    for i in com[2:]:
                        if any(c.isalpha() for c in com[2]):
                            subroutine_params.append(parsearg(i))
                case "ret":                                         # returns a value when block is called from subroutine (to the subroutine command) also stops exec of block     ret ?[val]
                    contdec = False
                    if any(c.isalpha() for c in com[1]):
                        return com[1]
                    return

                case "grv":                                         # gets subroutine values (when subroutine is called via a value-subroutine command)                             grv [out1] ?[out2] ?[out3] ?[out4] ....
                    c = 0
                    for i in subroutine_params:
                        try:
                            storeb(com[1+c], i)
                        except: pass
                        c += 1
                    subroutine_params = []

                case "iter":                                        # iterates over a given list. calls a subroutine with two args: [id] [elem]                                     iter [arr] [block]
                    l = parsearg(com[1])
                    c = 0
                    for i in l:
                        subroutine_params = [c, i]
                        decodeblock(com[2])
                        c += 1

                case "loop":                                        # loops X times. calls a subroutine with one arg: [iteration]                                                   loop [amount] [block]
                    l = parsearg(com[1])
                    c = 0
                    for i in range(l):
                        subroutine_params = [c]
                        decodeblock(com[2])
                        c += 1

                case "scmb":                                        # Combines multiple strings                                                                                     scmb [out] [in1: s] [in2: s] ?[in3: s] ....
                    s = ""
                    for i in com[2:]:
                        try:
                            s = s + parsearg(i)
                        except:
                            print("ERROR: Can only combine strings!")
                            sys.exit(-1)
                    storeb(com[1], s)

                case "conv":                                        # Converts a value                                                                                              conv [in] [type] [out]
                    i = parsearg(com[1])
                    o = None

                    match com[2]:
                        case "s":
                            o = str(i)
                        case "i":
                            o = int(i)
                        case "b":
                            o = bool(i)
                        case "a":
                            o = arrizeb(i)
                        case "f":
                            o = float(i)
                        case _:
                            print("ERROR: Type ",com[2], " not found!")
                            sys.exit(-1)
                    
                    storeb(com[3], o)

                case "aapp":                                         # Appends a value to a array                                                                                   aap [in] [element] [out]
                    il  = parsearg(com[1])
                    ie  = parsearg(com[2])
                    nl = il

                    nl.append(ie)

                    storeb(com[3], nl)

                case "clv":                                          # Clears a value (sets to none)                                                                                clv [out]
                    storeb(com[1], None)

                case "add":                                          # do simple math stuff (add)                                                                                   add [in1] [in2] [out]
                    i1 = parsearg(com[1])
                    i2 = parsearg(com[2])
                    o = i1 + i2

                    storeb(com[3], o)
                
                case "sub":                                          # do simple math stuff (sub)                                                                                   sub [in1] [in2] [out]
                    i1 = parsearg(com[1])
                    i2 = parsearg(com[2])
                    o = i1 - i2

                    storeb(com[3], o)

                case "mul":                                          # do simple math stuff (mul)                                                                                   mul [in1] [in2] [out]
                    i1 = parsearg(com[1])
                    i2 = parsearg(com[2])
                    o = i1 * i2

                    storeb(com[3], o)

                case "div":                                          # do simple math stuff (div)                                                                                   div [in1] [in2] [out]
                    i1 = parsearg(com[1])
                    i2 = parsearg(com[2])
                    o = i1 / i2

                    storeb(com[3], o)

                case "st":                                           # set type of variable                                                                                         st [out] [type]
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
                            print("ERROR: Type ",com[2], " not found!")
                            sys.exit(-1)
                    storeb(com[1], o)
                
                case "delay":                                        # waits for X seconds, then continues                                                                          delay [ms]
                    total_delay += parsearg(com[1])/1000
                    time.sleep(parsearg(com[1])/1000) 
                
                case "gentemp":                                      # generates temp variables                                                                                     gentemp [amount] ?[type]
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
                                print("ERROR: Type ",com[2], " not found!")
                                sys.exit(-1)
                        for i in range(parsearg(com[1])):
                            varlist.append("tmp"+str(i+tempvaramount))
                            varlistv.append(None)
                            storeb("vtmp"+str(i+tempvaramount), o)
                        tempvaramount += parsearg(com[1])
                            
                    else:
                        for i in range(parsearg(com[1])):
                            varlist.append("tmp"+str(i+tempvaramount))
                            varlistv.append(None)
                        
                case "repl":                                           # replaces a element (string) in a string                                                                    repl [what] [with] [string] [out]
                    s = parsearg(com[3])
                    o = s.replace(parsearg(com[1]), parsearg(com[2]))
                    storeb(com[4], o)

                case "eq":                                             # Jumps to a block if both inputs are equal                                                                  eq [block] [in1] [in2]
                    if parsearg(com[2]) == parsearg(com[3]):
                        contdec = False
                        decodeblock(com[1])

                case "neq":                                            # Jumps to a block if both inputs are not equal                                                              eq [block] [in1] [in2]
                    if not parsearg(com[2]) == parsearg(com[3]):
                        contdec = False
                        decodeblock(com[1])
                
                case "seq":                                             # Jumps to a subroutine if both inputs are equal                                                            eq [block] [in1] [in2] ?[out]
                    if parsearg(com[2]) == parsearg(com[3]):
                        t = decodeblock(com[1])
                        try:
                            if any(c.isalpha() for c in com[4]):
                                store(com[4], t)
                            else:
                                store("vtemp", t)
                        except:
                            store("vtemp", t)

                case "sneq":                                            # Jumps to a subroutine if both inputs are not equal                                                        eq [block] [in1] [in2] ?[out]
                    if not parsearg(com[2]) == parsearg(com[3]):
                        t = decodeblock(com[1])
                        try:
                            if any(c.isalpha() for c in com[4]):
                                store(com[4], t)
                            else:
                                store("vtemp", t)
                        except:
                            store("vtemp", t)

                case _:
                    pass

            line += 1

time_run_start = time.time()

decodeblock(0)

time_run_end = time.time()
time_total_end = time.time()

import os, psutil; used_mem = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2 * 1.049

print("\nProgramm Finished!\n")
print("dev data:")
print("runtime: PYTHON-3.10-STANDARD-INTERPRETER")
print("version: alpha.0.7 (08.01.2023)")
print("total variables: ",len(varlist))
print("- user variables: ",len(varlist)-tempvaramount)
print("- temp variables: ",tempvaramount)
print("total blocks: ",len(blocks))
print("total time: ",(time_total_end-time_total_start)* 1000," ms")
print("- decode time: ",(time_dec_end-time_dec_start)* 1000," ms")
print("- run time: ",(time_run_end-time_run_start)* 1000," ms")
print("- - run time (no delay): ",(time_run_end-time_run_start-total_delay)* 1000," ms (might be unaccurate when delay is used)")
print("used memory: ",used_mem," MB")
print("- runtime: ",14," MB (inaccurate)")
print("- interpreter: ",used_mem-14," MB (inaccurate)")