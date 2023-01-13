import sys

blocknames = []
blocks = []
varlist = []
varlistv = []
vartemp = None
subroutine_params = []
total_delay = 0
total_cinput_delay = 0

imported_blocks = []

tempvaramount = 0
file = "test.ssl"

def get_var_size():
    s = 0
    s += sys.getsizeof(blocknames)
    s += sys.getsizeof(blocks)
    s += sys.getsizeof(varlist)
    s += sys.getsizeof(varlistv)
    s += sys.getsizeof(vartemp)
    s += sys.getsizeof(subroutine_params)
    s += sys.getsizeof(total_delay)
    s += sys.getsizeof(total_cinput_delay)
    s += sys.getsizeof(imported_blocks)

    return s