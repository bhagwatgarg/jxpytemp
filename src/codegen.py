import sys
import copy
import csv
from math import log
from utilities import *
from tac import ST
import codecs
from lib import math_lib, print_int, scan_int
n_args = 0

leader_instr = [
    "ifgoto",
    "return",
    "label",
    "call",
    "print",
    "scan_int",
    "goto",
    "func",
]

relational_op_list = ['<','>','==','>=','<=']

class Codegen:

    def gen_data_section(self):
        
        print("default rel\n")
        print("extern malloc\n")
        print("extern printf\n")
        print("extern scanf\n")
        print("section\t.data\n")
        print('pint: db	"%ld", 10, 0')
        print('neg_: db "-"')
        print('sint: db	"%ld", 0')
        for var in symbol_table.keys():
            if is_temp_var(var):
                print(var + "\tdd\t0")

    def gen_start_template(self):
        print()
        print("section .text")
        print("\tglobal main")
        print(math_lib)
        print(print_int)
        print(scan_int)

    def op_binary(self,instr,op):

        R1, flag = get_reg(instr)
        if flag:
            print("\tmov"+ ' '+ R1 + ", " + get_location(instr.source1))
        R2 = get_location(instr.source2)
        print("\t"+op+ ' ' + R1 + ", " + R2)
        update_reg_desc(R1,instr.dest)
        if instr.source1!=instr.dest and instr.source2!=instr.dest:
            free_regs(instr)
    
    def op_fbinary(self,instr,op):

        R1, flag = get_reg(instr,isFloat=True)
        if flag:
            print("\tmovsd"+ ' '+ R1 + ", " + get_location(instr.source1))
        R2 = get_location(instr.source2)
        print("\t"+op+ ' ' + R1 + ", " + R2)
        update_reg_desc(R1,instr.dest)
        free_regs(instr)


    def op_add(self, instr):

        self.op_binary(instr,'add')


    def op_sub(self, instr):
        
        self.op_binary(instr,'sub')


    def op_mult(self, instr):

        R1, flag = get_reg(instr)
        if flag:
            print("\tmov "+ R1 + ", " + get_location(instr.source1))
        R2 = get_location(instr.source2)
        print("\timul " + R1 + ", " + R2)
        update_reg_desc(R1, instr.dest)
        free_regs(instr)


    def op_div(self, instr):

        save_reg("rax")
        print("\tmov rax, " + get_location(instr.source1))
        save_reg("rdx")
        if is_valid_number(instr.source2):
            R1, flag = get_reg(instr,exclude=["rax","rdx"])
            print("\tmov " + R1 + ", " + get_location(instr.source2))
            print("\tcdq")
            print("\tidiv " + R1)
        else:
            print("\tcdq")
            print("\tidiv " + get_location(instr.source2))
        update_reg_desc("rax", instr.dest)
        free_regs(instr)
    
    def op_fadd(self,instr):
        self.op_fbinary(instr,'addsd')

    def op_fsub(self,instr):
        self.op_fbinary(instr,'subsd')

    def op_fmul(self,instr):
        self.op_fbinary(instr, 'mulsd')

    def op_fdiv(self,instr):
        self.op_fbinary(instr, 'divsd')
    

    def op_frelational(self,instr,op):

        R1, flag = get_reg(instr,isFloat=True)
        if flag:
            save_reg(R1)
            print("\tmov"+ ' '+ R1 + ", " + get_location(instr.source1))
        R2 = get_location(instr.source2)
        R3, flag1 = get_reg(instr,isFloat=True)
        print("\t"+'ucomisd'+ ' ' + R1 + ", " + R2)

        temp_label = ST.make_label()
        temp_label2 = ST.make_label()
        if(op == "<"):
            print("\tjb " + temp_label)
        elif(op == ">"):
            print("\tja " + temp_label)
        elif(op == "=="):
            print("\tje " + temp_label)
        elif(op == "<="):
            print("\tjbe " + temp_label)
        elif(op == ">="):
            print("\tjae " + temp_label)
        print("\tmov " + R3 + ", 0")
        print("\tjmp " + temp_label2)
        print(temp_label + ":") 
        print("\tmov " + R3 + ", 1")
        print(temp_label2 + ":")

        update_reg_desc(R3,instr.dest)
        free_regs(instr)

    def op_relational(self,instr,op):

        R1, flag = get_reg(instr)
        if flag:
            save_reg(R1)
            print("\tmov"+ ' '+ R1 + ", " + get_location(instr.source1))
        R2 = get_location(instr.source2)
        print("\t"+'cmp'+ ' ' + R1 + ", " + R2)

        temp_label = ST.make_label()
        temp_label2 = ST.make_label()
        if(op == "<"):
            print("\tjl " + temp_label)
        elif(op == ">"):
            print("\tjg " + temp_label)
        elif(op == "=="):
            print("\tje " + temp_label)
        elif(op == "<="):
            print("\tjle " + temp_label)
        elif(op == ">="):
            print("\tjge " + temp_label)
        print("\tmov " + R1 + ", 0")
        print("\tjmp " + temp_label2)
        print(temp_label + ":") 
        print("\tmov " + R1 + ", 1")
        print(temp_label2 + ":")

        update_reg_desc(R1,instr.dest)
        free_regs(instr)

    def op_modulo(self, instr):

        save_reg("rax")
        print("\tmov rax, " + get_location(instr.source1))
        save_reg("rdx")
        if is_valid_number(instr.source2):
            R1, flag = get_reg(instr,exclude=["rax","rdx"])
            print("\tmov " + R1 + ", " + get_location(instr.source2))
            print("\tcdq")
            print("\tidiv " + R1)
        else:
            print("\tcdq")
            print("\tidiv " + get_location(instr.source2))

        update_reg_desc("rdx", instr.dest)
        free_regs(instr)


    def op_lshift(self, instr):

        R1, flag = get_reg(instr)
        if flag:
            print("\tmov "+ R1 + ", " + get_location(instr.source1))
        R2 = None
        if is_valid_number(instr.source2):
            R2 = instr.source2
        else:
            R2 = get_location(instr.source2)
        print("\tshl " + R1 + ", " + R2)
        update_reg_desc(R1, instr.dest)
        free_regs(instr)


    def op_rshift(self, instr):

        R1, flag = get_reg(instr)
        if flag:
            print("\tmov "+ R1 + ", " + get_location(instr.source1))
        R2 = None
        if is_valid_number(instr.source2):
            R2 = instr.source2
        else:
            R2 = get_location(instr.source2)
        print("\tshr " + R1 + ", " + R2)
        update_reg_desc(R1, instr.dest)
        free_regs(instr)

    def op_and(self,instr):
        self.op_binary(instr,'and')
    def op_or(self,instr):
        self.op_binary(instr,'or')
    def op_xor(self,instr):
        self.op_binary(instr,'xor')
    



    def op_intassign(self, instr):
        if is_valid_number(instr.source1):
            R1, flag = get_reg(instr, reg_nes=False)
            print("\tmov qword " + R1 + ", " + get_location(instr.source1))
            if R1 in reg_descriptor.keys():
                update_reg_desc(R1, instr.dest)

        else:
            if len(symbol_table[instr.source1].address_descriptor_reg) == 0:
                R1, flag = get_reg(instr)
                print("\tmov qword " + R1 +", " + get_location(instr.source1))
                update_reg_desc(R1,instr.source1)

            if len(symbol_table[instr.source1].address_descriptor_reg):
                for regs in symbol_table[instr.dest].address_descriptor_reg:
                    reg_descriptor[regs].remove(instr.dest)
                symbol_table[instr.dest].address_descriptor_reg.clear()
                symbol_table[instr.dest].address_descriptor_reg = copy.deepcopy(symbol_table[instr.source1].address_descriptor_reg)

                for reg in symbol_table[instr.dest].address_descriptor_reg:
                    reg_descriptor[reg].add(instr.dest)

                free_regs(instr)

        
    def op_fassign(self, instr):
        if  is_valid_float(instr.source1):
            R1, flag = get_reg(instr, reg_nes=False,isFloat=True)
            print("\tmovsd " + R1 + ", " + get_location(instr.source1))
            if R1 in reg_descriptor.keys():
                update_reg_desc(R1, instr.dest)

        else :
            if len(symbol_table[instr.source1].address_descriptor_reg) == 0:
                R1, flag = get_reg(instr)
                print("\tmov " + R1 +", " + get_location(instr.source1))
                update_reg_desc(R1,instr.source1)

            if len(symbol_table[instr.source1].address_descriptor_reg):
                for regs in symbol_table[instr.dest].address_descriptor_reg:
                    reg_descriptor[regs].remove(instr.dest)
                symbol_table[instr.dest].address_descriptor_reg.clear()
                symbol_table[instr.dest].address_descriptor_reg = copy.deepcopy(symbol_table[instr.source1].address_descriptor_reg)

                for reg in symbol_table[instr.dest].address_descriptor_reg:
                    reg_descriptor[reg].add(instr.dest)
                free_regs(instr)

        
    def op_unary(self, instr):
        R1, flag = get_reg(instr,reg_nes=False)
        if R1 not in reg_descriptor.keys():
            R1 = "qword " + R1
        if flag:
            print("\tmov "+ R1 + ", " + get_location(instr.source1))
        if instr.operation == "!" or instr.operation == "~":
            print("\tnot "+ R1)
        elif instr.operation == "++":
            print("\tinc "+ R1)
        elif instr.operation == "--":
            print("\tdec "+ R1)
        elif instr.operation == "-":
            print("\tneg "+ R1)
        if R1 in reg_descriptor.keys():
            update_reg_desc(R1,instr.dest)
        free_regs(instr)



    def op_ifgoto(self, instr):
        
        if(instr.source2=='eq0'):
            R1,flag = get_reg(instr,reg_nes=True)
            save_reg(R1)
            if flag:
                print("\tmov " + R1 + ", " + get_location(instr.source1))
            save_caller_context()
            print("\tcmp " + R1 + ", 0")
            print("\tje " + instr.dest)
        
        elif instr.source2=='eq0.0':
            R1,flag = get_reg(instr,reg_nes=True,isFloat=True)
            if flag:
                print("\tmovsd " + R1 + ", " + get_location(instr.source1))
            save_caller_context()
            print("\tucomisd " + R1 + ", "+ get_loc_mem('0.0'))
            print("\tje " + instr.dest)

        elif instr.source2=='eq0c':
            R1,flag = get_reg(instr,reg_nes=True)
            if flag:
                print("\tmov " + R1 + ", " + get_location(instr.source1))
            save_caller_context()
            print("\tcmp " + R1 + ", 0")
            print("\tje " + instr.dest)

        elif(instr.source2=='neq0'):
            R1,flag = get_reg(instr,reg_nes=True)
            save_reg(R1)
            if flag:
                print("\tmov " + R1 + ", " + get_location(instr.source1))
            save_caller_context()
            print("\tcmp " + R1 + ", 0")
            print("\tjne " + instr.dest)
        
        elif instr.source2=='neq0.0':
            R1,flag = get_reg(instr,reg_nes=True,isFloat=True)
            if flag:
                print("\tmovsd " + R1 + ", " + get_location(instr.source1))
            save_caller_context()
            print("\tucomisd " + R1 + ", "+ get_loc_mem('0.0'))
            print("\tjne " + instr.dest)

        elif instr.source2=='neq0c':
            R1,flag = get_reg(instr,reg_nes=True)
            if flag:
                print("\tmov " + R1 + ", " + get_location(instr.source1))
            save_caller_context()
            print("\tcmp " + R1 + ", 0")
            print("\tjne " + instr.dest)
            

    def op_goto(self, instr):
        save_caller_context()
        print("\tjmp " + instr.dest)

    def op_label(self, instr):
        save_caller_context()
        print(instr.dest + ":")

    def op_param(self, instr):
        global n_args
        if n_args==0:
            save_caller_context()
        n_args+=1
        print("\tpush " + str(get_location(instr.dest)))

    def op_pop(self, instr):
        global n_args
        n_args+=1
        print("\tpush " + str(get_location(instr.dest)))

    def op_call_function(self, instr):
        global n_args
        save_caller_context()
        print("\tcall " + instr.source1)
        print("\tadd rsp, " + str(8 * n_args))
        if instr.dest != None:
            update_reg_desc("rax",instr.dest)
        n_args = 0

    def op_return(self, instr):
        save_caller_context()
        if instr.source1 != None and instr.source1 != '':
            loc = get_location(instr.source1)
            save_reg("rax")
            if(loc != "rax"):
                print("\tmov rax, " + str(loc))

        print("\tmov rsp, rbp")
        print("\tpop rbp")
        print("\tret")

    def op_stack_alloc(self, instr):
        if instr.dest.split('$')[0] == 'main' :
            print("main:")
            print('\tmov rax,0',
        '\n\tpush rbp',
        '\n\tmov rbp, rsp',
        '\n\tpush rax',
        '\n\tcall malloc',
        '\n\tadd rsp, 8',
        '\n\tmov rsp, rbp',
        '\n\tpush rax',
        '\n\tcall Main$Main',
        '\n\tadd rsp, 8',
        '\n\tpush rax',
        '\n\tcall main$Main',
        '\n\tadd rsp, 8',
        '\n\tpop rbp',

        '\n\tret',)
        print(instr.dest + ":")
        counter = 0
        for i in symbol_table.keys():
            if not is_temp_var(i)  and not is_valid_float(i) and symbol_table[i].isArg == False:
                counter += 1
                symbol_table[i].address_descriptor_mem.add(-8 * counter)
                #print(instr.dest,i)
        sz=0
        for i, arg in enumerate(reversed(instr.arg_set)):
            if arg!='':
                sz+=8
                symbol_table[arg].address_descriptor_mem.add(sz + 16)
                #print('here',arg,sz+16)

        print("\tpush rbp")
        print("\tmov rbp, rsp")
        print("\tsub rsp, " + str(8*(counter + 10)))
        # TODO
        # print("\tsub rsp, " + "56")

    def op_declare(self, instr):
        loc = get_location(instr.source2)
        save_caller_context()
        if loc not in reg_descriptor.keys():
            print("\tmov rax," + loc)
            loc = "rax"
        # print("\tpush rbp")
        # print("\tmov rbp, rsp")
        print("\tpush " + loc)
        print("\tcall malloc")
        loc=symbol_table[instr.source1].address_descriptor_mem.pop()
        symbol_table[instr.source1].address_descriptor_mem.add(loc)
        print("\tmov [rbp",loc,"], rax") 
        print("\tadd rsp, 8")
        # print("\tmov rsp, rbp")
        # print("\tpop rbp")
        update_reg_desc("rax", instr.dest)

    def op_extract(self, instr):
        R1,flag = get_reg(instr)
        print("\tmov", R1, f", [rbp+16]")
        update_reg_desc(R1,instr.dest)

    def gen_code(self, instr):
        if instr.operation == "int_+":
            self.op_add(instr)
        elif instr.operation == "float_+":
            self.op_fadd(instr)
        elif instr.operation == "int_-":
            self.op_sub(instr)
        elif instr.operation == "float_-":
            self.op_fsub(instr)
        elif instr.operation == "int_*":
            self.op_mult(instr)
        elif instr.operation == "float_*":
            self.op_fmult(instr)
        elif instr.operation == "int_/":
            self.op_div(instr)
        elif instr.operation == "float_/":
            self.op_fdiv(instr)
        elif instr.operation == "int_%":
            self.op_modulo(instr)
        elif instr.operation == "int_<<":
            self.op_lshift(instr)
        elif instr.operation == "int_>>":
            self.op_rshift(instr)
        elif instr.operation != None and instr.operation.endswith('&'):
            self.op_and(instr)
        elif instr.operation != None and instr.operation.endswith('|'):
            self.op_or(instr)
        elif instr.operation != None and instr.operation.endswith('^'):
            self.op_xor(instr)
        elif instr.operation != None and (instr.operation.split("_")[-1] in relational_op_list and instr.operation.startswith("int")):
            self.op_relational(instr,instr.operation.split("_")[-1])
        elif instr.operation != None and (instr.operation.split("_")[-1] in relational_op_list and instr.operation.startswith("float")):
            self.op_frelational(instr,instr.operation.split("_")[-1])
        elif instr.operation in ['!','~','--','++','-']:
            self.op_unary(instr)
        
        elif instr.operation == "ifgoto":
            self.op_ifgoto(instr)

        elif instr.operation == "goto":
            self.op_goto(instr)

        elif instr.operation == "return":
            self.op_return(instr)

        elif instr.operation == "label":
            self.op_label(instr)

        elif instr.operation == "push":
            self.op_param(instr)

        elif instr.operation == "pop":
            self.op_pop(instr)

        elif instr.operation == "call":
            self.op_call_function(instr)
        
        elif instr.operation == "func":
            self.op_stack_alloc(instr)

        elif instr.operation != None and instr.operation.endswith('float_='):
            self.op_fassign(instr)
        
        elif instr.operation != None and instr.operation.endswith('_='):
            self.op_intassign(instr)

        elif instr.operation =='EXTRACT_THIS':
            self.op_extract(instr)

        elif instr.operation == "declare":
             self.op_declare(instr)

generator = Codegen()

def read_tac(filename):
    leader = set()
    leader.add(0)
    instructions_arr = []
    #with open(filename, 'r') as csvfile:
    instruction_set = list(csv.reader(codecs.open(filename, 'rU', 'utf-8')))
    j=1
    for i,statement in enumerate(instruction_set):
        if len(statement) == 0:
            continue
        instr = Instruction(statement)
        instructions_arr.append(instr)
        ex = 0
        if instr.operation in leader_instr:
            if instr.operation != "label"  and instr.operation != "func":
                ex += 1
            leader.add(j-1+ex)
        j+=1

    leader.add(len(instructions_arr))
    return (sorted(leader),instructions_arr)

def next_use(leader, instructions_arr):

    gen = Codegen()
    for block_start in range(len(leader) -  1):
        b_block = instructions_arr[leader[block_start] :leader[block_start + 1] ]
        j = leader[block_start + 1] - 1
        for instr in reversed(b_block):
            for sym in [instr.dest,instr.source1,instr.source2]:
                if is_valid_symbol(sym):
                    instr.inst_info['next_use'][sym] = copy.deepcopy(symbol_table[sym].next_use)
            for sym in [instr.dest,instr.source1,instr.source2]:
                if is_valid_symbol(sym):
                    instr.inst_info['live'][sym] = copy.deepcopy(symbol_table[sym].live)
            if is_valid_symbol(instr.dest):
                symbol_table[instr.dest].live = False
                symbol_table[instr.dest].next_use = None

            if is_valid_symbol(instr.source1):
                symbol_table[instr.source1].live = True
                symbol_table[instr.source1].next_use = j

            if is_valid_symbol(instr.source2):
                symbol_table[instr.source2].live = True
                symbol_table[instr.source2].next_use = j
            j-=1

        for instr in b_block:
            generator.gen_code(instr)
        reset_info()


def main():
    leader, instructions_arr = read_tac(sys.argv[1])
    generator.gen_data_section()
    generator.gen_start_template()
    next_use(leader, instructions_arr)

if __name__ == "__main__":
    try:
        main()
    except:
        sys.exit("Compilation failed! Wrong 3 Address Provided!")
