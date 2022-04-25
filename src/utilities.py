symbol_table = {}
reg_descriptor = {}
reg_descriptor["rax"] = set()
reg_descriptor["rbx"] = set()
reg_descriptor["rcx"] = set()
reg_descriptor["rdx"] = set()
reg_descriptor["rsi"] = set()
reg_descriptor["rdi"] = set()


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

def reset_info():
    for symbol in symbol_table.keys():
        symbol_table[symbol].live = True
        symbol_table[symbol].next_use = None
    return symbol_table

def is_valid_number(symbol):
    if len(symbol)>0 and symbol[0] == "-":
        return True
    return symbol.isdigit()

def is_valid_symbol(symbol):
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
    def __init__(self,isArr = False, size = 0 ,array_size=0,isArg=False):
        # self.value = None
        self.live = True
        self.next_use = None
        self.array_size = array_size
        self.isArr = isArr
        self.isArg = isArg
        self.address_descriptor_mem = set()
        self.address_descriptor_reg = set()


class Instruction:
    def __init__(self, statement):
        self.source1 = None
        self.source2= None
        self.dest = None
        self.operation = None
        self.inst_info = {}
        self.inst_info['next_use'] = {}
        self.inst_info['live'] ={}
        self.arg_set = []
        self.get_info(statement)
        symbols = [self.source1, self.dest, self. source2]
        #print(self.arg_set)
        for symbol in symbols:
            if is_valid_symbol(symbol) and symbol not in symbol_table.keys():
                symbol_table[symbol] = symbol_data()
        for symbol in self.arg_set:
            if is_valid_symbol(symbol) and symbol not in symbol_table.keys():
                symbol_table[symbol] = symbol_data(isArg=True)
    
    def extract_args(self,args):
        # args
        args= args.split(':')[::-1]
        return args

    def get_info(self, statement):
        if statement[0] == "ifgoto":
            self.operation = 'ifgoto'
            self.source1= statement[1]
            self.source2= statement[2]
            self.dest = statement[3]

        elif statement[0] == "goto":
            self.operation = 'goto'
            self.dest = statement[3]

        elif statement[0] == "push":
            self.operation = statement[0]
            self.dest = statement[1]

        elif statement[3] == "declare":
            self.operation = statement[3]
            self.dest = statement[0]
            self.source1 = statement[1]
            self.source2= statement[2]

        elif statement[0] == "call":
            self.operation = "call"
            self.dest = statement[3] 
            self.source1 = statement[1]
        
        elif statement[0] == "label :":
            self.operation = 'label'
            self.dest = statement[3]

        elif statement[0] == "func":
            self.operation = "func"
            self.dest = statement[1]
            self.arg_set = self.extract_args(statement[2])

        elif statement[0] == "ret":
            self.operation = "return"
            self.source1 = statement[1]
        
        elif statement[0] == 'pop':
            self.operation = "pop"
            self.source1 = statement[1]

        elif statement[3] == "int_float_=":
            self.operation = 'i2f'
            self.dest = statement[0]
            self.source1 = statement[1]

        elif statement[3] == "float_int_=":
            self.operation = 'f2i'
            self.dest = statement[0]
            self.source1 = statement[1]
        
        elif statement[1] == 'EXTRACT_THIS':
            self.operation = statement[1]
            self.dest = statement[0]

        elif statement[3] == "char_int_=":
            self.operation = 'c2i'
            self.dest = statement[0]
            self.source1 = statement[1]
        
        elif statement[3] == "int_char_=":
            self.operation = 'i2c'
            self.dest = statement[0]
            self.source1 = statement[1]

        elif statement[3] == "char_float_=":
            self.operation = 'c2f'
            self.dest = statement[0]
            self.source1 = statement[1]

        elif statement[3] == "float_char_=":
            self.operation = 'f2c'
            self.dest = statement[0]
            self.source1 = statement[1]

        elif statement[3] == "float_=" or statement[3] == "float_float_=" or statement[3] == "int_=" or statement[3] == "int_int_=" or statement[3] == "char_char_=" or statement[3] == "char_=":
            self.operation = statement[3]
            self.dest = statement[0]
            self.source1 = statement[1]
        
        elif statement[3] == 'DEREFERENCE':
            self.operation = statement[3]
            self.dest = statement[0]
            self.source1 = statement[2] 

        elif statement[3] in ["|", "||", "&", "&&", "^", "~", "!"]:
            self.source1= statement[1]
            self.source2= statement[2]
            self.dest= statement[0]
            self.operation = statement[3]

        elif statement[3].startswith("int_") or statement[3].startswith("float_") or statement[3].startswith("char_"):
            self.operation = statement[3]
            self.source1= statement[1]
            self.source2= statement[2]
            self.dest = statement[0]


def get_loc_mem(symbol,flag=1):

    if not is_valid_symbol(symbol):
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
    if is_valid_symbol(symbol) == False:
        return
    reg_descriptor[register].add(symbol)
    for reg in symbol_table[symbol].address_descriptor_reg:
        if register != reg:
            reg_descriptor[reg].remove(symbol)
    symbol_table[symbol].address_descriptor_reg.clear()
    symbol_table[symbol].address_descriptor_reg.add(register)


def free_regs(instr):
    if is_valid_symbol(instr.source1):
        if instr.inst_info['next_use'][instr.source1] == None and instr.inst_info['live'][instr.source1] == False:
            treg=''
            for reg in symbol_table[instr.source1].address_descriptor_reg:
                reg_descriptor[reg].remove(instr.source1)
                treg=reg
            symbol_table[instr.source1].address_descriptor_reg.clear()
            if is_val_reg(treg):
                if treg.startswith('xmm'):
                    print("\tmovsd qword " + get_loc_mem(instr.source1) + ", " + treg)
                else:
                    print("\tmov qword " + get_loc_mem(instr.source1) + ", " + treg)
            #print('aaaaa',treg)
    if is_valid_symbol(instr.source2):
            if instr.inst_info['next_use'][instr.source1] == None and instr.inst_info['live'][instr.source1] == False:
                treg = ''
                for reg in symbol_table[instr.source2].address_descriptor_reg:
                    reg_descriptor[reg].remove(instr.source2)
                    treg=reg
                symbol_table[instr.source2].address_descriptor_reg.clear()
                if is_val_reg(treg):
                    if treg.startswith('xmm'):
                        print("\tmovsd qword " + get_loc_mem(instr.source2) + ", " + treg)
                    else:
                        print("\tmov qword " + get_loc_mem(instr.source2) + ", " + reg)

def get_location(symbol,exclude_reg=[]):

    if not is_valid_symbol(symbol):
        return symbol

    if is_valid_symbol(symbol):
        for reg in symbol_table[symbol].address_descriptor_reg:
            if reg not in exclude_reg:
                return reg
        if is_temp_var(symbol):
            for reg in reg_descriptor.keys():
                if symbol in reg_descriptor[reg]:
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
                    print("\tmov qword " + get_loc_mem(symbol) + ", " + str(reg))
                symbol_table[symbol].address_descriptor_reg.clear()
                saved.add(symbol)
        reg_descriptor[reg].clear()


def save_reg(reg):
    for symbol in reg_descriptor[reg]:
        for loc in symbol_table[symbol].address_descriptor_mem:
            if reg.startswith('xmm'):
                print("\tmovsd "+ get_loc_mem(symbol) + ", " + reg)
            else:
                print("\tmov qword " + get_loc_mem(symbol) + ", " + reg)
        symbol_table[symbol].address_descriptor_reg.remove(reg)
    reg_descriptor[reg].clear()


def get_reg(instr, reg_nes=True, exclude=[],isFloat=False):

    if not isFloat:
        if is_valid_symbol(instr.dest):
            if is_valid_symbol(instr.source1):
                for reg in symbol_table[instr.source1].address_descriptor_reg:
                    if reg not in exclude:
                        if len(reg_descriptor[reg]) == 1 and instr.inst_info['next_use'][instr.source1]== None and not reg.startswith('xmm'):
                            save_reg(reg)
                            return reg, False

            for reg in reg_descriptor.keys():
                if reg not in exclude and not reg.startswith('xmm'):
                    if len(reg_descriptor[reg]) == 0:
                        save_reg(reg)
                        return reg, True

            if reg_nes or (instr.source1 in instr.inst_info['next_use'].keys() and instr.inst_info['next_use'][instr.source1]):
                R = None
                for reg in reg_descriptor.keys():
                    if reg not in exclude:
                        if R==None:
                            R=reg
                        elif len(reg_descriptor[reg])<len(reg_descriptor[R]):
                            R=reg
                save_reg(R)
                return R, True

            else:
                return get_loc_mem(instr.dest), False
    
