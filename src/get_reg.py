from utilities import *

reg_descriptor = {}
byte={}
reg_descriptor["eax"] = set()
reg_descriptor["ebx"] = set()
reg_descriptor["ecx"] = set()
reg_descriptor["edx"] = set()
reg_descriptor["esi"] = set()
reg_descriptor["edi"] = set()
reg_descriptor["xmm0"] = set()
reg_descriptor["xmm1"] = set()
reg_descriptor["xmm2"] = set()
reg_descriptor["xmm3"] = set()
reg_descriptor["xmm4"] = set()
reg_descriptor["xmm5"] = set()
reg_descriptor["xmm6"] = set()
reg_descriptor["xmm7"] = set()
byte["eax"] = "al"
byte["ebx"] = "bl"
byte["ecx"] = "cl"
byte["edx"] = "dl"
byte["esi"] = "sil"
byte["edi"] = "dil"

def get_loc_mem(symbol,flag=1):

    if not is_valid_sym(symbol):
        return symbol

    if len(symbol_table[symbol].address_descriptor_mem)==0:
        return symbol

    for loc in symbol_table[symbol].address_descriptor_mem:
        break
    if type(loc) == int:
        if loc > 0 :
            if flag:
                return "[ebp+" + str(loc) + "]"
            else:
                return 'ebp+'+ str(loc)
        else:
            if flag:
                return "[ebp" + str(loc) + "]"
            else:
                return 'ebp'+ str(loc)           
    else:
        if flag:
            return "[" + loc + "]"
        else:
            return loc


def update_reg_desc(register,symbol):
    reg_descriptor[register].clear()
    if is_valid_sym(symbol) == False:
        return
    reg_descriptor[register].add(symbol)
    for reg in symbol_table[symbol].address_descriptor_reg:
        if register != reg:
            reg_descriptor[reg].remove(symbol)
    symbol_table[symbol].address_descriptor_reg.clear()
    symbol_table[symbol].address_descriptor_reg.add(register)

def free_regs(instr):
    if is_valid_sym(instr.inp1):
        if instr.inst_next_use[instr.inp1].next_use == None and instr.inst_live[instr.inp1].live == False:
            for reg in symbol_table[instr.inp1].address_descriptor_reg:
                reg_descriptor[reg].remove(instr.inp1)
            symbol_table[instr.inp1].address_descriptor_reg.clear()
            if is_val_reg(reg):
                if reg.startswith(xmm):
                    print("\tmovss dword " + get_loc_mem(instr.inp1) + ", " + reg)
                else:
                    print("\tmov dword " + get_loc_mem(instr.inp1) + ", " + reg)

    if is_valid_sym(instr.inp2):
            if instr.inst_next_use[instr.inp2].next_use == None and instr.inst_live[instr.inp2].live == False:
                for reg in symbol_table[instr.inp2].address_descriptor_reg:
                    reg_descriptor[reg].remove(instr.inp2)
                symbol_table[instr.inp2].address_descriptor_reg.clear()
                if is_val_reg(reg):
                    if reg.startswith(xmm):
                        print("\tmovss dword " + get_loc_mem(instr.inp2) + ", " + reg)
                    else:
                        print("\tmov dword " + get_loc_mem(instr.inp2) + ", " + reg)

def get_location(symbol,exclude_reg=[],isByte=False):

    if not is_valid_sym(symbol):
        return symbol

    if is_valid_sym(symbol):
        for reg in symbol_table[symbol].address_descriptor_reg:
            if reg not in exclude_reg:
                if isByte:
                    return byte[reg]
                else:
                    return reg

    if isByte:
        return 'byte'+ get_loc_mem(symbol)
    else:
        return 'dword' + get_loc_mem(symbol)

def save_caller_context():
    saved = set()
    for reg, symbols in reg_descriptor.items():
        for symbol in symbols:
            if symbol not in saved:
                if reg.startswith('xmm'):
                    print("\tmovss " + get_loc_mem(symbol) + ", " + str(reg))
                else :
                    print("\tmov " + get_loc_mem(symbol) + ", " + str(reg))
                symbol_table[symbol].address_descriptor_reg.clear()
                saved.add(symbol)
        reg_descriptor[reg].clear()


def save_reg(reg):
    for symbol in reg_descriptor[reg]:
        for loc in symbol_table[symbol].address_descriptor_mem:
            if reg.startswith('xmm'):
                print("\tmovss "+ get_loc_mem(symbol) + ", " + reg)
            else:
                print("\tmov " + get_loc_mem(symbol) + ", " + reg)
        symbol_table[symbol].address_descriptor_reg.remove(reg)
    reg_descriptor[reg].clear()


def get_reg(instr, compulsory=True, exclude=[],isFloat=False):
    '''
    Uses next use heuristic to allocate registers
    Returns 2 values:
    1. R1: The best register for inp1
    2. flag: boolean to know whether a register has to be allocated to inp1
    '''
    if not isFloat:
        if is_valid_sym(instr.out):
            if is_valid_sym(instr.inp1):
                for reg in symbol_table[instr.inp1].address_descriptor_reg:
                    if reg not in exclude:
                        if len(reg_descriptor[reg]) == 1 and instr.inst_next_use[instr.inp1].next_use == None and not instr.inst_live[instr.inp1].live and ((not reg.startswith('xmm')):
                            symbol_table[instr.inp1].address_descriptor_reg.remove(reg)
                            return reg, False

            for reg in reg_descriptor.keys():
                if reg not in exclude and ((not reg.startswith('xmm')):
                    if len(reg_descriptor[reg]) == 0:
                        return reg, True

            if compulsory or instr.inst_next_use[instr.out].next_use:
                R = None
                next_use = -1000000
                for reg in reg_descriptor.keys():
                    if reg not in exclude and ((not reg.startswith('xmm')):
                        to_break = False
                        for sym in reg_descriptor[reg]:
                            n_use = instr.inst_next_use[sym].next_use
                            if n_use and n_use > next_use:
                                if n_use:
                                    next_use = n_use
                                R = reg
                            if not n_use:
                                R = reg
                                to_break = True
                                break
                        if to_break:
                            break
                save_reg(R)
                return R, True

            else:
                return get_loc_mem(instr.out), False
    else :

        if is_valid_sym(instr.out):
            if is_valid_sym(instr.inp1):
                for reg in symbol_table[instr.inp1].address_descriptor_reg:
                    if reg not in exclude:
                        if len(reg_descriptor[reg]) == 1 and instr.inst_next_use[instr.inp1].next_use == None and not instr.inst_live[instr.inp1].live and ((reg.startswith('xmm')):
                            symbol_table[instr.inp1].address_descriptor_reg.remove(reg)
                            return reg, False

            for reg in reg_descriptor.keys():
                if reg not in exclude and ((reg.startswith('xmm')):
                    if len(reg_descriptor[reg]) == 0:
                        return reg, True

            if compulsory or instr.inst_next_use[instr.out].next_use:
                R = None
                next_use = -1000000
                for reg in reg_descriptor.keys():
                    if reg not in exclude and ((reg.startswith('xmm')):
                        to_break = False
                        for sym in reg_descriptor[reg]:
                            n_use = instr.inst_next_use[sym].next_use
                            if n_use and n_use > next_use:
                                if n_use:
                                    next_use = n_use
                                R = reg
                            if not n_use:
                                R = reg
                                to_break = True
                                break
                        if to_break:
                            break
                save_reg(R)
                return R, True

            else:
                return get_loc_mem(instr.out), False
