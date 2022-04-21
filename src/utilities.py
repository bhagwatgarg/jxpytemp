from os import stat
import sys
import csv

leader_ins = [
    "ifgoto",
    "return",
    "label",
    "call",
    "goto",
    "func",
    "begin_func",
    "end_func"
]


symbol_table = {}

def is_val_reg(reg):
    return reg in reg_descriptor.keys()

def is_temp_var(symbol):
    if symbol[0] == "_":
        return True
    return False

def reset_live_and_next_use():
    for symbol in symbol_table.keys():
        symbol_table[symbol].live = True
        symbol_table[symbol].next_use = None
    return symbol_table

def is_valid_number(symbol):
    if symbol[0] == "-":
        return True
    return symbol.isdigit()

def is_valid_sym(symbol):
    if type(symbol) != type(''):
        return False
    # elif symbol != None and symbol[0] == "'" and symbol[-1] == "'" and len(symbol) > 2:
    #     return False
    # elif symbol != None and symbol[0] == "`" and symbol[-1] == "`" and len(symbol) > 3:
    #     return False
    elif symbol != None and not is_valid_number(symbol):
        return True
    return False

class symbol_data:
    def __init__(self,isArr = False, size = 0 ,array_size=0):
        # self.value = None
        self.live = True
        self.next_use = None
        self.array_size = array_size
        self.isArr = isArr
        self.size = (size+3//4)*4
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
        self.inst_info = dict()
        self.get_info(statement)
        self.populate_per_inst_next_use()
        self.arg_set = []


    def extract(self, symbol):

        index = symbol.find("[")
        if index != -1:
            return symbol[:index], symbol[index + 1:-1]
        else:
            return symbol, None
    
    def extract_args(self,args):

        if(len(args)==2):
            return []
        if(len(args)==3):
            return [args[1]]
        else:
            args = args[1:-2]
            return args.split(',')

    def get_info(self, statement):
        '''
        Populate appropriate entries of Instruction class
        according to instruction type
        '''
        if statement[0] == "ifgoto":
            # 10, ifgoto, leq, a, 50, 2
            self.operation = 'ifgoto'
            self.inp1, self.array_index_i1 = self.extract(statement[1].strip())
            self.inp2, self.array_index_i2 = self.extract(statement[2].strip())
            self.out = statement[3]

        elif statement[0] == "goto":
            self.operation = 'goto'
            self.out = statement[3]

        elif statement[0] == "push":
            self.operation = statement[0]
            self.out = statement[1]

        elif statement[0] == "call":
            self.operation = "call"
            self.out = statement[3]   #TODO add temp for retval in emit
            self.inp1 = statement[1]
        
        elif statement[0] == "label":
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
            self.operation = "return"
            self.inp1 = statement[1]

        elif statement[3] == "int_float_=":
            self.operation = statement[3]
            self.out = statement[0]
            self.inp1 = statement[1]

        elif statement[3] == "float_int_=":
            self.operation = statement[3]
            self.out = statement[0]
            self.inp1 = statement[1]

        elif statement[3] == "char_int_=":
            self.operation = statement[3]
            self.out = statement[0]
            self.inp1 = statement[1]
        
        elif statement[3] == "int_char_=":
            self.operation = statement[3]
            self.out = statement[0]
            self.inp1 = statement[1]

        elif statement[3] == "char_float_=":
            self.operation = statement[3]
            self.out = statement[0]
            self.inp1 = statement[1]

        elif statement[3] == "float_char_=":
            self.operation = statement[3]
            self.out = statement[0]
            self.inp1 = statement[1]

        

        elif statement[0] in ["~","!","++","--"]:
            #10, ++, out, variable
            self.operation = instr_type
            self.instr_type = "unary"
            self.inp1, self.array_index_i1 = self.handle_array_notation(statement[-1].strip())
            self.out, self.array_index_o = self.handle_array_notation(statement[2].strip())
            self.add_to_symbol_table([
                self.inp1, self.array_index_i1,
                self.out, self.array_index_o
            ])


        elif instr_type == "=":
            # 10, =, a, 2
            self.instr_type = "assignment"
            self.operation = "="
            self.inp1, self.array_index_i1 = self.handle_array_notation(statement[-1].strip())
            self.out, self.array_index_o = self.handle_array_notation(statement[2].strip())
            self.add_to_symbol_table([
                self.inp1, self.array_index_i1,
                self.out, self.array_index_o
            ])



        elif instr_type in ["|", "||", "&", "&&", "^", "~", "!"]:
            # 10, &&, a, a, b
            self.instr_type = "logical"
            self.inp1, self.array_index_i1 = self.handle_array_notation(statement[3].strip())
            self.inp2, self.array_index_i2 = self.handle_array_notation(statement[4].strip())
            self.out, self.array_index_o = self.handle_array_notation(statement[2].strip())
            self.add_to_symbol_table([
                self.inp1, self.array_index_i1,
                self.inp2, self.array_index_i2,
                self.out, self.array_index_o
            ])
            self.operation = statement[1].strip()

        else:
            # 10, +, a, a, b
            self.instr_type = "arithmetic"
            self.inp1, self.array_index_i1 = self.handle_array_notation(statement[3].strip())
            self.inp2, self.array_index_i2 = self.handle_array_notation(statement[4].strip())
            self.out, self.array_index_o = self.handle_array_notation(statement[2].strip())
            self.add_to_symbol_table([
                self.inp1, self.array_index_i1,
                self.inp2, self.array_index_i2,
                self.out, self.array_index_o
            ])
            self.operation = statement[1].strip()


    def populate_per_inst_next_use(self):
        '''
        for each symbol in instruction, initialize the next use
        and liveness parameters
        '''
        symbols = [
                self.inp1, self.array_index_i1,
                self.inp2, self.array_index_i2,
                self.out, self.array_index_o
            ]
        for symbol in symbols:
            if is_valid_sym(symbol):
                self.inst_info[symbol] = symbol_info()


def read_three_address_code(filename):
    '''
    Given a csv file `filename`, read the file
    and find the basic blocks. Also store each instruction
    as an instance of Instruction class in a list `IR_code`
    '''
    leader = set()
    leader = [0]
    IR_code = []
    j=1

    with open(filename, 'r') as csvfile:
        instruction_set = list(csv.reader(csvfile, delimiter=','))
        index_label_to_be_added = set()
        for i,statement in enumerate(instruction_set):
            if len(statement) == 0:
                continue
            IR = Instruction(statement)
            IR_code.append(IR)
            instr_type = IR.instr_type

            instr_type = IR_code[i].instr_type
            line_no = 0
            if instr_type in leader_instructions:
                if instr_type != "label" and instr_type != "print_int" and instr_type != "scan_int" and instr_type != "func":
                    line_no += 1

                leader.append(j-1+line_no)
            j+=1
    leader.add(len(IR_code))

    return (sorted(leader), IR_code)