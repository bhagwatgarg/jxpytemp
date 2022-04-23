symbol_table = {}

def is_val_reg(reg):
    return reg in reg_descriptor.keys()

def is_valid_float(potential_float):
    try:
        float(potential_float)

        return True
    except ValueError:
        return False

def is_temp_var(symbol):
    if len(symbol)>0 and symbol[0] == "_":
        return True
    return False

def reset_live_and_next_use():
    for symbol in symbol_table.keys():
        symbol_table[symbol].live = True
        symbol_table[symbol].next_use = None
    return symbol_table

def is_valid_number(symbol):
    if len(symbol)>0 and symbol[0] == "-":
        return True
    return symbol.isdigit()

def is_valid_sym(symbol):
    if type(symbol) != type(''):
        return False
    # elif symbol != None and symbol[0] == "'" and symbol[-1] == "'" and len(symbol) > 2:
    #     return False
    # elif symbol != None and symbol[0] == "`" and symbol[-1] == "`" and len(symbol) > 3:
    #     return False
    elif symbol != None and not is_valid_number(symbol) and not is_valid_float(symbol):
        return True
    return False

class symbol_data:
    def __init__(self,isArr = False, size = 0 ,array_size=0):
        # self.value = None
        self.live = True
        self.next_use = None
        self.array_size = array_size
        self.isArr = isArr
#       self.size = (size+3//4)*4
        self.address_descriptor_mem = set()
        self.address_descriptor_reg = set()


class Instruction:
    def __init__(self, statement):
        self.inp1 = None
        self.array_index_i1 = None
        self.inp2 = None
        self.array_index_i2 = None
        self.out = None
        self.array_index_o = None
        self.operation = None
        self.inst_info = {}
        self.inst_info['next_use'] = {}
        self.inst_info['live'] ={}
        self.arg_set = []
        self.get_info(statement)
        symbols = [
                self.inp1, self.array_index_i1,
                self.inp2, self.array_index_i2,
                self.out, self.array_index_o
            ]
        for symbol in symbols:
            if is_valid_sym(symbol):
                symbol_table[symbol] = symbol_data()
        for symbol in self.arg_set:
            if is_valid_sym(symbol):
                symbol_table[symbol] = symbol_data()

    def extract(self, symbol):

        index = symbol.find("[")
        if index != -1:
            return symbol[:index], symbol[index + 1:-1]
        else:
            return symbol, None
    
    def extract_args(self,args):
        # args
        args= args.strip('][').split(', ')
        args=[arg[1:-1] for arg in args]
        return args

    def get_info(self, statement):
        '''
        Populate appropriate entries of Instruction class
        according to instruction type
        '''
        if statement[0] == "ifgoto":
            # 10, ifgoto, leq, a, 50, 2
            self.operation = 'ifgoto'
            self.inp1, self.array_index_i1 = self.extract(statement[1])
            self.inp2, self.array_index_i2 = self.extract(statement[2])
            self.out = statement[3]

        elif statement[0] == "goto":
            self.operation = 'goto'
            self.out = statement[3]

        elif statement[0] == "push":
            self.operation = statement[0]
            self.out = statement[1]

        elif statement[3] == "declare":
            self.operation = statement[3]
            self.out = statement[0]
            self.inp1 = statement[1]
            self.inp2 = statement[2]

        elif statement[0] == "call":
            self.operation = "call"
            self.out = statement[3]   #TODO add temp for retval in emit
            self.inp1 = statement[1]
        
        elif statement[0] == "label :":
            self.operation = 'label'
            self.out = statement[3]

        elif statement[0] == "func":
            self.operation = "func"
            self.out = statement[1]
            self.arg_set = self.extract_args(statement[2])

        elif statement[0] == "ret":
            self.operation = "return"
            self.inp1 = statement[1]
        
        elif statement[0] == 'pop':
            self.operation = "pop"
            self.inp1 = statement[1]

        elif statement[3] == "int_float_=":
            self.operation = 'i2f'
            self.out = statement[0]
            self.inp1 = statement[1]

        elif statement[3] == "float_int_=":
            self.operation = 'f2i'
            self.out = statement[0]
            self.inp1 = statement[1]
        
        elif statement[1] == 'EXTRACT_THIS':
            self.operation = statement[1]
            self.out = statement[0]

        elif statement[3] == "char_int_=":
            self.operation = 'c2i'
            self.out = statement[0]
            self.inp1 = statement[1]
        
        elif statement[3] == "int_char_=":
            self.operation = 'i2c'
            self.out = statement[0]
            self.inp1 = statement[1]

        elif statement[3] == "char_float_=":
            self.operation = 'c2f'
            self.out = statement[0]
            self.inp1 = statement[1]

        elif statement[3] == "float_char_=":
            self.operation = 'f2c'
            self.out = statement[0]
            self.inp1 = statement[1]

        elif statement[3] == "float_=" or statement[3] == "float_float_=" or statement[3] == "int_=" or statement[3] == "int_int_=" or statement[3] == "char_char_=" or statement[3] == "char_=":
            self.operation = statement[3]
            self.out = statement[0]
            self.inp1 = statement[1]
        
        elif statement[3] == 'DEREFERENCE':
            self.operation = statement[3]
            self.out = statement[0]
            self.inp1 = statement[2]
        
        # elif statement[3] == "float_neg":
        #     self.operation = statement[3]
        #     self.out = statement[0]
        #     self.inp1 = statement[1]
        
        # elif statement[3] == "int_neg":
        #     self.operation = statement[3]
        #     self.out = statement[0]
        #     self.inp1 = statement[1]

        elif statement[3] in ["|", "||", "&", "&&", "^", "~", "!"]:
            self.inp1, self.array_index_i1 = self.extract(statement[1])
            self.inp2, self.array_index_i2 = self.extract(statement[2])
            self.out, self.array_index_o = self.extract(statement[0])
            self.operation = statement[3]

        elif statement[3].startswith("int_") or statement[3].startswith("float_") or statement[3].startswith("char_"):
            self.operation = statement[3]
            self.inp1, self.array_index_i1 = self.extract(statement[1])
            self.inp2, self.array_index_i2 = self.extract(statement[2])
            self.out, self.array_index_o = self.extract(statement[0])


reg_descriptor = {}
reg_descriptor["rax"] = set()
reg_descriptor["rbx"] = set()
reg_descriptor["rcx"] = set()
reg_descriptor["rdx"] = set()
reg_descriptor["rsi"] = set()
reg_descriptor["rdi"] = set()
reg_descriptor["xmm0"] = set()
reg_descriptor["xmm1"] = set()
reg_descriptor["xmm2"] = set()
reg_descriptor["xmm3"] = set()
reg_descriptor["xmm4"] = set()
reg_descriptor["xmm5"] = set()
reg_descriptor["xmm6"] = set()
reg_descriptor["xmm7"] = set()

def get_loc_mem(symbol,flag=1):

    if not is_valid_sym(symbol):
        return symbol

    if len(symbol_table[symbol].address_descriptor_mem)==0:
        #print('aaaaaaaaa')
        return symbol

    for loc in symbol_table[symbol].address_descriptor_mem:
        break
    if type(loc) == type(1):
        if loc > 0 :
            if flag:
                return "[rbp+" + str(loc) + "]"
            else:
                return 'rbp+'+ str(loc)
        else:
            if flag:
                return "[rbp" + str(loc) + "]"
            else:
                return 'rbp'+ str(loc)           
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
        if instr.inst_info['next_use'][instr.inp1] == None and instr.inst_info['live'][instr.inp1] == False:
            treg=''
            for reg in symbol_table[instr.inp1].address_descriptor_reg:
                reg_descriptor[reg].remove(instr.inp1)
                treg=reg
            symbol_table[instr.inp1].address_descriptor_reg.clear()
            if is_val_reg(treg):
                if treg.startswith('xmm'):
                    print("\tmovsd qword " + get_loc_mem(instr.inp1) + ", " + treg)
                else:
                    print("\tmov qword " + get_loc_mem(instr.inp1) + ", " + treg)
            #print('aaaaa',treg)
    if is_valid_sym(instr.inp2):
            if instr.inst_info['next_use'][instr.inp1] == None and instr.inst_info['live'][instr.inp1] == False:
                treg = ''
                for reg in symbol_table[instr.inp2].address_descriptor_reg:
                    reg_descriptor[reg].remove(instr.inp2)
                    treg=reg
                symbol_table[instr.inp2].address_descriptor_reg.clear()
                if is_val_reg(treg):
                    if treg.startswith('xmm'):
                        print("\tmovsd qword " + get_loc_mem(instr.inp2) + ", " + treg)
                    else:
                        print("\tmov qword " + get_loc_mem(instr.inp2) + ", " + reg)

def get_location(symbol,exclude_reg=[]):

    if not is_valid_sym(symbol):
        return symbol

    if is_valid_sym(symbol):
        for reg in symbol_table[symbol].address_descriptor_reg:
            if reg not in exclude_reg:
                return reg
        return 'qword ' + get_loc_mem(symbol)

def save_caller_context():
    saved = set()
    for reg, symbols in reg_descriptor.items():
        for symbol in symbols:
            if symbol not in saved and not is_temp_var(symbol):
                if reg.startswith('xmm'):
                    print("\tmovsd " + get_loc_mem(symbol) + ", " + str(reg))
                else :
                    print("\tmov " + get_loc_mem(symbol) + ", " + str(reg))
                symbol_table[symbol].address_descriptor_reg.clear()
                saved.add(symbol)
        reg_descriptor[reg].clear()


def save_reg(reg):
    for symbol in reg_descriptor[reg]:
        for loc in symbol_table[symbol].address_descriptor_mem:
            if reg.startswith('xmm'):
                print("\tmovsd "+ get_loc_mem(symbol) + ", " + reg)
            else:
                print("\tmov " + get_loc_mem(symbol) + ", " + reg)
        symbol_table[symbol].address_descriptor_reg.remove(reg)
    reg_descriptor[reg].clear()


def get_reg(instr, compulsory=True, exclude=[],isFloat=False):

    if not isFloat:
        if is_valid_sym(instr.out):
            if is_valid_sym(instr.inp1):
                for reg in symbol_table[instr.inp1].address_descriptor_reg:
                    if reg not in exclude:
                        if len(reg_descriptor[reg]) == 1 and instr.inst_info['next_use'][instr.inp1]== None and not instr.inst_info['live'][instr.inp1] and not reg.startswith('xmm'):
                            save_reg(reg)
                            return reg, False

            for reg in reg_descriptor.keys():
                if reg not in exclude and not reg.startswith('xmm'):
                    if len(reg_descriptor[reg]) == 0:
                        save_reg(reg)
                        return reg, True

            if compulsory or instr.inst_info['next_use'][instr.inp1]:
                R = None
                next_use = -1000000
                for reg in reg_descriptor.keys():
                    if reg not in exclude and not reg.startswith('xmm'):
                        to_break = False
                        for sym in reg_descriptor[reg]:
                            n_use = instr.inst_info['next_use'][instr.inp1]
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
                        if len(reg_descriptor[reg]) == 1 and instr.inst_info['next_use'][instr.inp1] == None and not instr.inst_info['live'][instr.inp1] and reg.startswith('xmm'):
                            save_reg(reg)
                            return reg, False

            for reg in reg_descriptor.keys():
                if reg not in exclude and reg.startswith('xmm'):
                    if len(reg_descriptor[reg]) == 0:
                        save_reg(reg)
                        return reg, True

            if compulsory or instr.inst_next_use[instr.out].next_use:
                R = None
                next_use = -1000000
                for reg in reg_descriptor.keys():
                    if reg not in exclude and reg.startswith('xmm'):
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
