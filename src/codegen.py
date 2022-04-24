import sys
import copy
import csv
from math import log
from utilities import *
from tac import ST
import codecs
param_count = 0

leader_instructions = [
    "ifgoto",
    "return",
    "label",
    "call",
    "print",
    "scan_int",
    "goto",
    "func",
    "begin_func",
    "end_func"
]
relational_op_list = ['<','>','==','>=','<=']

class CodeGenerator:

    def gen_data_section(self):
        
        print("default rel\n")
        print("extern malloc\n")
        print("extern printf\n")
        print("extern scanf\n")
        print("section\t.data\n")
        print('pint: db	"%ld ", 0')
        print('sint: db	"%ld", 0')
        #print("print_char:\tdb\t\"%c\",0")
        #print("scan_int:\tdb\t\"%d\",0")
        for var in symbol_table.keys():
            if is_temp_var(var):
                print(var + "\tdd\t0")
        # for symbol in symbol_table.keys():
            # if symbol_table[symbol].array_size != None:
                # print(str(symbol) + "\ttimes\t" + str(symbol_table[symbol].array_size) + "\tdd\t0")
            # else:
                # print(str(symbol) + "\tdd\t0")

    def gen_start_template(self):
        print()
        print("section .text")
        print("\tglobal main")

        print("print$Imports$int:	\n\tpush rbp\n\tmov rbp, rsp\n\tpush rsi\n\tpush rdi\n\tmov rsi, qword [rbp+24]\n\tlea rdi, [rel pint]\n\txor rax, rax\n\tcall printf\n\txor rax, rax\n\tpop rsi\n\tpop rdi\n\tmov rsp, rbp\n\tpop rbp\n\tret")
        print("""scan_int$Imports:
\tpush rbp
\tmov rbp, rsp
\tpush rsi
\tpush rdi
\tadd rsp, 8
\tmov rsi, rsp
\tlea rdi, [rel sint]
\txor rax, rax
\tcall scanf
\tmov rax, qword [rsp]
\tpop rdi
\tpop rsi
\tmov rsp, rbp
\tpop rbp
\tret
        """)
    # def op_print(self, instr):
    #     loc = get_location(instr.inp1)
    #     save_caller_context()
    #     if loc not in reg_descriptor.keys():
    #         print("\tmov rax, " + loc)
    #         loc = "rax"
    #     print("\tpush rbp")
    #     print("\tmov rbp,esp")
    #     print("\tpush qword " + str(loc))
    #     print("\tpush qword print")
    #     print("\tcall printf")
    #     print("\tadd esp, 8")
    #     print("\tmov esp, rbp")
    #     print("\tpop rbp")

    # def op_print_char(self, instr):
    #     loc = get_location(instr.inp1)
    #     save_caller_context()
    #     if loc not in reg_descriptor.keys():
    #         print("\tmov rax, " + loc)
    #         loc = "rax"
    #     print("\tpush rbp")
    #     print("\tmov rbp,esp")
    #     print("\tpush qword " + str(loc))
    #     print("\tpush qword print_char")
    #     print("\tcall printf")
    #     print("\tadd esp, 8")
    #     print("\tmov esp, rbp")
    #     print("\tpop rbp")

    # def op_scan_int(self, instr):
    #     save_caller_context()
    #     loc = get_location(instr.out)
    #     print("\tlea rax, " + loc)
    #     print("\tpush rbp")
    #     print("\tmov rbp,esp")
    #     print("\tpush rax")
    #     print("\tpush scan_int")
    #     print("\tcall scanf")
    #     print("\tadd esp, 8")
    #     print("\tmov esp, rbp")
    #     print("\tpop rbp")

    # def optimize_if_possible(self, out, inp1, inp2, op):
    #     '''
    #     If both inputs are integers; compute them beforehand
    #     '''
    #     if is_valid_number(inp1) and is_valid_number(inp2):
    #         inp1 = int(inp1)
    #         inp2 = int(inp2)
    #         if op == "+":
    #             res = inp1 + inp2
    #         elif op == "-":
    #             res = inp1 - inp2
    #         elif op == "*":
    #             res = inp1 * inp2
    #         elif op == "/":
    #             res = inp1 / inp2
    #         elif op == "%":
    #             res = inp1 % inp2
    #         elif op == "<<":
    #             res = inp1 << inp2
    #         elif op == ">>":
    #             res = inp1 >> inp2
    #         res = int(res)
    #         print("\tmov " + get_location(out) + ", " + get_location(str(res)))
    #         return True
    #     return False

    def op_binary(self,instr,op):

        R1, flag = get_reg(instr)
        if flag:
            print("\tmov"+ ' '+ R1 + ", " + get_location(instr.inp1))
        R2 = get_location(instr.inp2)
        print("\t"+op+ ' ' + R1 + ", " + R2)
        update_reg_desc(R1,instr.out)
        if instr.inp1!=instr.out and instr.inp2!=instr.out:
            free_regs(instr)
    
    def op_fbinary(self,instr,op):

        R1, flag = get_reg(instr,isFloat=True)
        if flag:
            print("\tmovsd"+ ' '+ R1 + ", " + get_location(instr.inp1))
        R2 = get_location(instr.inp2)
        print("\t"+op+ ' ' + R1 + ", " + R2)
        update_reg_desc(R1,instr.out)
        free_regs(instr)


    def op_add(self, instr):

        self.op_binary(instr,'add')


    def op_sub(self, instr):
        
        self.op_binary(instr,'sub')


    def op_mult(self, instr):

        R1, flag = get_reg(instr)
        if flag:
            print("\tmov "+ R1 + ", " + get_location(instr.inp1))
        # handle cases when inp2 is a power of 2
        bitshift = False        # to avoid multiple operation
        if is_valid_number(instr.inp2):
            num = int(instr.inp2)
            if num & (num - 1) == 0 and num != 0:
                # use bitshift
                power = int(log(int(instr.inp2)))
                print("\tshl " + R1 + ", " + str(power))
                bitshift = False
        if not bitshift:
            R2 = get_location(instr.inp2)
            print("\timul " + R1 + ", " + R2)
        update_reg_desc(R1, instr.out)
        free_regs(instr)


    def op_div(self, instr):

        save_reg("rax")
        print("\tmov rax, " + get_location(instr.inp1))
        save_reg("rdx")
        if is_valid_number(instr.inp2):
            R1, flag = get_reg(instr,exclude=["rax","rdx"])
            print("\tmov " + R1 + ", " + get_location(instr.inp2))
            print("\tcdq")
            print("\tidiv " + R1)
        else:
            print("\tcdq")
            print("\tidiv qword " + get_location(instr.inp2))
        update_reg_desc("rax", instr.out)
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
            print("\tmov"+ ' '+ R1 + ", " + get_location(instr.inp1))
        R2 = get_location(instr.inp2)
        R3, flag1 = get_reg(instr,isFloat=True)
        print("\t"+'ucomisd'+ ' ' + R1 + ", " + R2)

        lbl = ST.make_label()
        if(op == "<"):
            print("\tjb " + lbl)
        elif(op == ">"):
            print("\tja " + lbl)
        elif(op == "=="):
            print("\tje " + lbl)
        elif(op == "!="):
            print("\tjne " + lbl)
        elif(op == "<="):
            print("\tjbe " + lbl)
        elif(op == ">="):
            print("\tjae " + lbl)
        print("\tmov " + R3 + ", 0")
        lbl2 = ST.make_label()
        print("\tjmp " + lbl2)
        print(lbl + ":") 
        print("\tmov " + R3 + ", 1")
        print(lbl2 + ":")

        update_reg_desc(R3,instr.out)
        free_regs(instr)

    def op_relational(self,instr,op):

        R1, flag = get_reg(instr)
        if flag:
            save_reg(R1)
            print("\tmov"+ ' '+ R1 + ", " + get_location(instr.inp1))
        R2 = get_location(instr.inp2)
        print("\t"+'cmp'+ ' ' + R1 + ", " + R2)

        lbl = ST.make_label()
        if(op == "<"):
            print("\tjl " + lbl)
        elif(op == ">"):
            print("\tjg " + lbl)
        elif(op == "=="):
            print("\tje " + lbl)
        elif(op == "!="):
            print("\tjne " + lbl)
        elif(op == "<="):
            print("\tjle " + lbl)
        elif(op == ">="):
            print("\tjge " + lbl)
        print("\tmov " + R1 + ", 0")
        lbl2 = ST.make_label()
        print("\tjmp " + lbl2)
        print(lbl + ":") 
        print("\tmov " + R1 + ", 1")
        print(lbl2 + ":")

        update_reg_desc(R1,instr.out)
        free_regs(instr)

    def op_modulo(self, instr):

        save_reg("rax")
        print("\tmov rax, " + get_location(instr.inp1))
        save_reg("rdx")
        if is_valid_number(instr.inp2):
            R1, flag = get_reg(instr,exclude=["rax","rdx"])
            print("\tmov " + R1 + ", " + get_location(instr.inp2))
            print("\tcdq")
            print("\tidiv " + R1)
        else:
            print("\tcdq")
            print("\tidiv qword" + get_location(instr.inp2))

        update_reg_desc("rdx", instr.out)
        free_regs(instr)


    def op_lshift(self, instr):

        R1, flag = get_reg(instr)
        if flag:
            print("\tmov "+ R1 + ", " + get_location(instr.inp1))
        R2 = None
        if is_valid_number(instr.inp2):
            R2 = instr.inp2
        else:
            R2 = get_location(instr.inp2)
        print("\tshl " + R1 + ", " + R2)
        update_reg_desc(R1, instr.out)
        free_regs(instr)


    def op_rshift(self, instr):

        R1, flag = get_reg(instr)
        if flag:
            print("\tmov "+ R1 + ", " + get_location(instr.inp1))
        R2 = None
        if is_valid_number(instr.inp2):
            R2 = instr.inp2
        else:
            R2 = get_location(instr.inp2)
        print("\tshr " + R1 + ", " + R2)
        update_reg_desc(R1, instr.out)
        free_regs(instr)

    def op_and(self,instr):
        self.op_binary(instr,'and')
    def op_or(self,instr):
        self.op_binary(instr,'or')
    def op_xor(self,instr):
        self.op_binary(instr,'xor')
    



    def op_intassign(self, instr):
        if instr.array_index_i1 == None and instr.array_index_o == None and is_valid_number(instr.inp1):
            R1, flag = get_reg(instr, compulsory=False)
            print("\tmov  " + R1 + ", " + get_location(instr.inp1))
            if R1 in reg_descriptor.keys():
                update_reg_desc(R1, instr.out)

        elif instr.array_index_i1 == None and instr.array_index_o == None:
            if len(symbol_table[instr.inp1].address_descriptor_reg) == 0:
                R1, flag = get_reg(instr)
                print("\tmov  " + R1 +", " + get_location(instr.inp1))
                update_reg_desc(R1,instr.inp1)

            if len(symbol_table[instr.inp1].address_descriptor_reg):
                for regs in symbol_table[instr.out].address_descriptor_reg:
                    reg_descriptor[regs].remove(instr.out)
                symbol_table[instr.out].address_descriptor_reg.clear()
                symbol_table[instr.out].address_descriptor_reg = copy.deepcopy(symbol_table[instr.inp1].address_descriptor_reg)

                for reg in symbol_table[instr.out].address_descriptor_reg:
                    reg_descriptor[reg].add(instr.out)

                free_regs(instr)

        # elif instr.array_index_i1 != None:
        #     # assert len(symbol_table[instr.inp1].address_descriptor_reg) == 0
        #     R1, flag = get_reg(instr)
        #     print("\tmov " + R1 + ", " + get_location(instr.array_index_i1))
        #     print("\tshl " + R1 + ", 2")
        #     print("\tadd " + R1 + ", " + get_location(instr.inp1))
        #     print("\tmov " + R1 + ", [" + R1 + "]")
        #     update_reg_desc(R1, instr.out)
        
        # elif instr.array_index_i1 != None and instr.array_index_o != None:
            
        #     index1 = instr.array_index_i1
        #     loc_arr1 = get_location(instr.inp1)
        #     R3 = None
        #     R4 = None
        #     if loc_arr1 in reg_descriptor.keys():
        #         R1 = None
        #         if is_valid_sym(index1):
        #             if len(symbol_table[index].address_descriptor_reg) == 0:
        #                 R1, _ = get_reg(instr, exclude=[loc_arr1])
        #                 print("\tmov " + R1 + ", " + get_location(index1))
        #                 update_reg_desc(R1, index1)
        #             else:
        #                 R1 = get_location(index1)
        #             R3 = R1
        #         else:
        #             index1 = 4 * int(index1)
        #     else:
        #         R1, _ = get_reg(instr)
        #         print("\tmov " + R1 + ", " + get_location(index1))
        #         print("\tshl " + R1 + ", 2")
        #         print("\tadd " + R1 + ", " + loc_arr1)
        #         R4 = R1
            

        #     index = instr.array_index_o
        #     loc_arr = get_location(instr.out)
        #     if loc_arr in reg_descriptor.keys():
        #         R1 = None
        #         if is_valid_sym(index):
        #             if len(symbol_table[index].address_descriptor_reg) == 0:
        #                 R1, _ = get_reg(instr, exclude=[loc_arr])
        #                 print("\tmov " + R1 + ", " + get_location(index))
        #                 update_reg_desc(R1, index)
        #             else:
        #                 R1 = get_location(index)

        #             if R3:
        #                 print("\tmov [" + loc_arr + "," + R1 + "*4], " + "[" + loc_arr1 + "," + R3 + "*4]" )
        #             elif R4:
        #                 print("\tmov [" + loc_arr + "," + R1 + "*4], " + "[" + R4 + "]" )
        #             else:
        #                 print("\tmov [" + loc_arr + "," + R1 + "*4], " + "[" + loc_arr + "+" + str(index1) + "]" )
        #         else:
        #             index = 4 * int(index)
        #             inp_reg, flag = get_reg(instr)
        #             if flag:
        #                 print("\tmov " + inp_reg + ", " + get_location(instr.inp1))
        #                 update_reg_desc(inp_reg,instr.inp1)
        #             if R3:
        #                 print("\tmov [" + loc_arr + "+" + str(index) + "], " + "[" + loc_arr1 + "," + R3 + "*4]" )
        #             elif R4:
        #                 print("\tmov [" + loc_arr + "+" + str(index) + "], " + "[" + R4 + "]" )
        #             else:
        #                 print("\tmov [" + loc_arr + "+" + str(index) + "], " + "[" + loc_arr + "+" + str(index1) + "]" )

        #     else:
        #         R1, _ = get_reg(instr, exclude=[loc_inp1])
        #         print("\tmov " + R1 + ", " + get_location(index))
        #         print("\tshl " + R1 + ", 2")
        #         print("\tadd " + R1 + ", " + loc_arr)
        #         # print("\tmov [" + R1 + "], " + loc_inp1)
        #         if R3:
        #             print("\tmov [" + R1 + "], " + "[" + loc_arr1 + "," + R3 + "*4]" )
        #         elif R4:
        #             print("\tmov [" + R1 + "], " + "[" + R4 + "]" )
        #         else:
        #             print("\tmov [" + R1 + "], " + "[" + loc_arr + "+" + str(index1) + "]" )


        # else:
        #     index = instr.array_index_o
        #     loc_arr = get_location(instr.out)
        #     if loc_arr in reg_descriptor.keys():
        #         R1 = None
        #         if is_valid_sym(index):
        #             if len(symbol_table[index].address_descriptor_reg) == 0:
        #                 R1, _ = get_reg(instr, exclude=[loc_arr])
        #                 print("\tmov " + R1 + ", " + get_location(index))
        #                 update_reg_desc(R1, index)
        #             else:
        #                 R1 = get_location(index)

        #             inp_reg = R1
        #             if index != instr.inp1:
        #                 inp_reg, flag = get_reg(instr, exclude=[R1, loc_arr])
        #                 if flag:
        #                     print("\tmov " + inp_reg + ", " + get_location(instr.inp1))
        #                     update_reg_desc(inp_reg,instr.inp1)
        #             print("\tmov [" + loc_arr + "," + R1 + "*4], " + inp_reg)
        #         else:
        #             index = 4 * int(index)
        #             inp_reg, flag = get_reg(instr)
        #             if flag:
        #                 print("\tmov " + inp_reg + ", " + get_location(instr.inp1))
        #                 update_reg_desc(inp_reg,instr.inp1)
        #             print("\tmov [" + loc_arr + "+" + str(index) + "], " + inp_reg)
        #     else:
        #         loc_inp1 = get_location(instr.inp1)
        #         R1, _ = get_reg(instr, exclude=[loc_inp1])
        #         print("\tmov " + R1 + ", " + get_location(index))
        #         print("\tshl " + R1 + ", 2")
        #         print("\tadd " + R1 + ", " + loc_arr)
        #         if loc_inp1 in reg_descriptor.keys():
        #             print("\tmov [" + R1 + "], " + loc_inp1)
        #         else:
        #             inp_reg, _ = get_reg(instr, exclude=[R1])
        #             print("\tmov " + inp_reg + ", " + loc_inp1)
        #             update_reg_desc(inp_reg, instr.inp1)
        #             print("\tmov [" + R1 + "], " + inp_reg)
    
    def op_fassign(self, instr):
        if instr.array_index_i1 == None and instr.array_index_o == None and is_valid_float(instr.inp1):
            R1, flag = get_reg(instr, compulsory=False,isFloat=True)
            print("\tmovsd " + R1 + ", " + get_location(instr.inp1))
            if R1 in reg_descriptor.keys():
                update_reg_desc(R1, instr.out)

        elif instr.array_index_i1 == None and instr.array_index_o == None:
            if len(symbol_table[instr.inp1].address_descriptor_reg) == 0:
                R1, flag = get_reg(instr)
                print("\tmov " + R1 +", " + get_location(instr.inp1))
                update_reg_desc(R1,instr.inp1)

            if len(symbol_table[instr.inp1].address_descriptor_reg):
                for regs in symbol_table[instr.out].address_descriptor_reg:
                    reg_descriptor[regs].remove(instr.out)
                symbol_table[instr.out].address_descriptor_reg.clear()
                symbol_table[instr.out].address_descriptor_reg = copy.deepcopy(symbol_table[instr.inp1].address_descriptor_reg)

                for reg in symbol_table[instr.out].address_descriptor_reg:
                    reg_descriptor[reg].add(instr.out)

                free_regs(instr)

        # elif instr.array_index_i1 != None:
        #     # assert len(symbol_table[instr.inp1].address_descriptor_reg) == 0
        #     R1, flag = get_reg(instr)
        #     print("\tmov " + R1 + ", " + get_location(instr.array_index_i1))
        #     print("\tshl " + R1 + ", 2")
        #     print("\tadd " + R1 + ", " + get_location(instr.inp1))
        #     print("\tmov " + R1 + ", [" + R1 + "]")
        #     update_reg_desc(R1, instr.out)
        
        # elif instr.array_index_i1 != None and instr.array_index_o != None:
            
        #     index1 = instr.array_index_i1
        #     loc_arr1 = get_location(instr.inp1)
        #     R3 = None
        #     R4 = None
        #     if loc_arr1 in reg_descriptor.keys():
        #         R1 = None
        #         if is_valid_sym(index1):
        #             if len(symbol_table[index].address_descriptor_reg) == 0:
        #                 R1, _ = get_reg(instr, exclude=[loc_arr1])
        #                 print("\tmov " + R1 + ", " + get_location(index1))
        #                 update_reg_desc(R1, index1)
        #             else:
        #                 R1 = get_location(index1)
        #             R3 = R1
        #         else:
        #             index1 = 4 * int(index1)
        #     else:
        #         R1, _ = get_reg(instr)
        #         print("\tmov " + R1 + ", " + get_location(index1))
        #         print("\tshl " + R1 + ", 2")
        #         print("\tadd " + R1 + ", " + loc_arr1)
        #         R4 = R1
            

        #     index = instr.array_index_o
        #     loc_arr = get_location(instr.out)
        #     if loc_arr in reg_descriptor.keys():
        #         R1 = None
        #         if is_valid_sym(index):
        #             if len(symbol_table[index].address_descriptor_reg) == 0:
        #                 R1, _ = get_reg(instr, exclude=[loc_arr])
        #                 print("\tmov " + R1 + ", " + get_location(index))
        #                 update_reg_desc(R1, index)
        #             else:
        #                 R1 = get_location(index)

        #             if R3:
        #                 print("\tmov [" + loc_arr + "," + R1 + "*4], " + "[" + loc_arr1 + "," + R3 + "*4]" )
        #             elif R4:
        #                 print("\tmov [" + loc_arr + "," + R1 + "*4], " + "[" + R4 + "]" )
        #             else:
        #                 print("\tmov [" + loc_arr + "," + R1 + "*4], " + "[" + loc_arr + "+" + str(index1) + "]" )
        #         else:
        #             index = 4 * int(index)
        #             inp_reg, flag = get_reg(instr)
        #             if flag:
        #                 print("\tmov " + inp_reg + ", " + get_location(instr.inp1))
        #                 update_reg_desc(inp_reg,instr.inp1)
        #             if R3:
        #                 print("\tmov [" + loc_arr + "+" + str(index) + "], " + "[" + loc_arr1 + "," + R3 + "*4]" )
        #             elif R4:
        #                 print("\tmov [" + loc_arr + "+" + str(index) + "], " + "[" + R4 + "]" )
        #             else:
        #                 print("\tmov [" + loc_arr + "+" + str(index) + "], " + "[" + loc_arr + "+" + str(index1) + "]" )

        #     else:
        #         R1, _ = get_reg(instr, exclude=[loc_inp1])
        #         print("\tmov " + R1 + ", " + get_location(index))
        #         print("\tshl " + R1 + ", 2")
        #         print("\tadd " + R1 + ", " + loc_arr)
        #         # print("\tmov [" + R1 + "], " + loc_inp1)
        #         if R3:
        #             print("\tmov [" + R1 + "], " + "[" + loc_arr1 + "," + R3 + "*4]" )
        #         elif R4:
        #             print("\tmov [" + R1 + "], " + "[" + R4 + "]" )
        #         else:
        #             print("\tmov [" + R1 + "], " + "[" + loc_arr + "+" + str(index1) + "]" )


        # else:
        #     index = instr.array_index_o
        #     loc_arr = get_location(instr.out)
        #     if loc_arr in reg_descriptor.keys():
        #         R1 = None
        #         if is_valid_sym(index):
        #             if len(symbol_table[index].address_descriptor_reg) == 0:
        #                 R1, _ = get_reg(instr, exclude=[loc_arr])
        #                 print("\tmov " + R1 + ", " + get_location(index))
        #                 update_reg_desc(R1, index)
        #             else:
        #                 R1 = get_location(index)

        #             inp_reg = R1
        #             if index != instr.inp1:
        #                 inp_reg, flag = get_reg(instr, exclude=[R1, loc_arr])
        #                 if flag:
        #                     print("\tmov " + inp_reg + ", " + get_location(instr.inp1))
        #                     update_reg_desc(inp_reg,instr.inp1)
        #             print("\tmov [" + loc_arr + "," + R1 + "*4], " + inp_reg)
        #         else:
        #             index = 4 * int(index)
        #             inp_reg, flag = get_reg(instr)
        #             if flag:
        #                 print("\tmov " + inp_reg + ", " + get_location(instr.inp1))
        #                 update_reg_desc(inp_reg,instr.inp1)
        #             print("\tmov [" + loc_arr + "+" + str(index) + "], " + inp_reg)
        #     else:
        #         loc_inp1 = get_location(instr.inp1)
        #         R1, _ = get_reg(instr, exclude=[loc_inp1])
        #         print("\tmov " + R1 + ", " + get_location(index))
        #         print("\tshl " + R1 + ", 2")
        #         print("\tadd " + R1 + ", " + loc_arr)
        #         if loc_inp1 in reg_descriptor.keys():
        #             print("\tmov [" + R1 + "], " + loc_inp1)
        #         else:
        #             inp_reg, _ = get_reg(instr, exclude=[R1])
        #             print("\tmov " + inp_reg + ", " + loc_inp1)
        #             update_reg_desc(inp_reg, instr.inp1)
        #             print("\tmov [" + R1 + "], " + inp_reg)
    

    def op_unary(self, instr):
        R1, flag = get_reg(instr,compulsory=False)
        if R1 not in reg_descriptor.keys():
            R1 = "qword " + R1
        if flag:
            print("\tmov "+ R1 + ", " + get_location(instr.inp1))
        if instr.operation == "!" or instr.operation == "~":
            print("\tnot "+ R1)
        elif instr.operation == "++":
            print("\tinc "+ R1)
        elif instr.operation == "--":
            print("\tdec "+ R1)
        elif instr.operation == "-":
            print("\tneg "+ R1)
        if R1 in reg_descriptor.keys():
            update_reg_desc(R1,instr.out)
        free_regs(instr)

    def int2float(self, instr):
        R1,flag = get_reg(instr, isFloat=True)
        update_reg_desc(R1,instr.out)
        print("\tcvtsi2ss " + R1 + ", " +  get_location(instr.inp1))


    def float2int(self, instr):
        R1,flag = get_reg(instr)
        update_reg_desc(R1,instr.out)
        print("\tcvttss2si " + R1 + ", " +  get_location(instr.inp1))


    def char2int(self, instr):
        R1,flag = get_reg(instr,exclude=['esi','edi'])
        print("\txor " + R1  + ", " + R1)
        print("\tmov " + R1 + ", " + get_location(instr.inp1))
        update_reg_desc(R1,instr.out)


    def char2float(self, instr):
        R1,flag = get_reg(instr,exclude=['esi','edi'])
        print("\txor " + R1 + ", " + R1)
        print("\tmov " + R1 +", " + get_location(instr.inp1))
        R2,flag2 = get_reg(instr, isFloat=True)
        update_reg_desc(R2, instr.out)
        print("\tcvtsi2ss " + R2 + ", " + R1)


    def int2char(self, instr):
        R1,flag = get_reg(instr,  exclude = ["rsi", "rdi"])
        R2,flag2 = get_reg(instr, exclude = [R1, "rsi", "rdi"])
        print("\tmov " + R1 +", " + get_location(instr.inp1))
        update_reg_desc(R2, instr.out)
        print("\txor " + R2 + ", " + R2)
        print("\tmov " + R2 + ", " + R1)


    def float2char(self, instr):
        R1 = get_reg(instr, isFloat=True)
        print("\tmovsd " + R1 + ", " + get_location(instr.inp1))
        R2 = get_reg(instr)
        print("\tcvttss2si " + R2  + ", " + R1)
        R3 = get_reg(instr, exclude = [R2, "rsi", "rdi"])
        print("\txor " + R3 + ", " + R3)
        print("\tmov " + R3 + ", " + R2)
        update_reg_desc(R3, instr.out)


    def op_ifgoto(self, instr):
        
        if(instr.inp2=='eq0'):
            R1,flag = get_reg(instr,compulsory=True)
            save_reg(R1)
            if flag:
                print("\tmov " + R1 + ", " + get_location(instr.inp1))
            save_caller_context()
            print("\tcmp " + R1 + ", 0")
            print("\tje " + instr.out)
        
        elif instr.inp2=='eq0.0':
            R1,flag = get_reg(instr,compulsory=True,isFloat=True)
            if flag:
                print("\tmovsd " + R1 + ", " + get_location(instr.inp1))
            save_caller_context()
            print("\tucomisd " + R1 + ", "+ get_loc_mem('0.0'))
            print("\tje " + instr.out)

        elif instr.inp2=='eq0c':
            R1,flag = get_reg(instr,compulsory=True)
            if flag:
                print("\tmov " + R1 + ", " + get_location(instr.inp1))
            save_caller_context()
            print("\tcmp " + R1 + ", 0")
            print("\tje " + instr.out)

        elif(instr.inp2=='neq0'):
            R1,flag = get_reg(instr,compulsory=True)
            save_reg(R1)
            if flag:
                print("\tmov " + R1 + ", " + get_location(instr.inp1))
            save_caller_context()
            print("\tcmp " + R1 + ", 0")
            print("\tjne " + instr.out)
        
        elif instr.inp2=='neq0.0':
            R1,flag = get_reg(instr,compulsory=True,isFloat=True)
            if flag:
                print("\tmovsd " + R1 + ", " + get_location(instr.inp1))
            save_caller_context()
            print("\tucomisd " + R1 + ", "+ get_loc_mem('0.0'))
            print("\tjne " + instr.out)

        elif instr.inp2=='neq0c':
            R1,flag = get_reg(instr,compulsory=True)
            if flag:
                print("\tmov " + R1 + ", " + get_location(instr.inp1))
            save_caller_context()
            print("\tcmp " + R1 + ", 0")
            print("\tjne " + instr.out)
            

    def op_goto(self, instr):
        save_caller_context()
        print("\tjmp " + instr.out)

    def op_label(self, instr):
        save_caller_context()
        print(instr.out + ":")

    def op_param(self, instr):
        global param_count
        if param_count==0:
            save_caller_context()
        param_count+=1
        print("\tpush " + str(get_location(instr.out)))

    def op_pop(self, instr):
        global param_count
        param_count+=1
        print("\tpush " + str(get_location(instr.out)))

    def op_call_function(self, instr):
        global param_count
        save_caller_context()
        print("\tcall " + instr.inp1)
        print("\tadd rsp, " + str(8 * param_count))
        if instr.out != None:
            update_reg_desc("rax",instr.out)
        param_count = 0

    def op_return(self, instr):
        save_caller_context()
        if instr.inp1 != None and instr.inp1 != '':
            loc = get_location(instr.inp1)
            save_reg("rax")
            if(loc != "rax"):
                print("\tmov rax, " + str(loc))

        print("\tmov rsp, rbp")
        print("\tpop rbp")
        print("\tret")

    def op_stack_alloc(self, instr):
        if instr.out.split('$')[0] == 'main' :
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
        print(instr.out + ":")
        counter = 0
        for i in symbol_table.keys():
            if not is_temp_var(i)  and not is_valid_float(i) and symbol_table[i].isArg == False:
                counter += 1
                symbol_table[i].address_descriptor_mem.add(-8 * counter)
                #print(instr.out,i)
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
        loc = get_location(instr.inp2)
        save_caller_context()
        if loc not in reg_descriptor.keys():
            print("\tmov rax," + loc)
            loc = "rax"
        # print("\tpush rbp")
        # print("\tmov rbp, rsp")
        print("\tpush " + loc)
        print("\tcall malloc")
        loc=symbol_table[instr.inp1].address_descriptor_mem.pop()
        symbol_table[instr.inp1].address_descriptor_mem.add(loc)
        print("\tmov [rbp",loc,"], rax") 
        print("\tadd rsp, 8")
        print("\tmov rsp, rbp")
        print("\tpop rbp")
        update_reg_desc("rax", instr.out)

    def op_extract(self, instr):
        R1,flag = get_reg(instr)
        print("\tmov", R1, f", [rbp+16]")
        update_reg_desc(R1,instr.out)

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
        # elif instr.operation == "int_+=":
        #     instr.operation = 'int_+'
        #     self.op_add(instr)
        #     instr.operation = 'int_='
        #     self.op_intassign(instr)
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
        
        elif instr.operation =='f2i':
            self.float2int(instr)

        elif instr.operation =='i2f':
            self.int2float(instr)
        
        elif instr.operation =='c2i':
            self.char2int(instr)
        
        elif instr.operation =='i2c':
            self.int2char(instr)

        elif instr.operation =='EXTRACT_THIS':
            self.op_extract(instr)

        # elif instr_type == "print":
        #     self.op_print(instr)

        # elif instr_type == "print_char":
        #     self.op_print_char(instr)

        # elif instr_type == "scan_int":
        #     self.op_scan_int(instr)


        # elif instr_type == "begin_func":
        #     self.op_stack_alloc(instr)
            # for sym, symentry in symbol_table.items():
                # print(sym, symentry.address_descriptor_mem)

        elif instr.operation == "declare":
             self.op_declare(instr)


###################################global generator############################
generator = CodeGenerator()
###################################global generator############################
def read_three_address_code(filename):
    leader = set()
    leader.add(0)
    IR_code = []
    #with open(filename, 'r') as csvfile:
    instruction_set = list(csv.reader(codecs.open(filename, 'rU', 'utf-8')))
    j=1
    for i,statement in enumerate(instruction_set):
        if len(statement) == 0:
            continue
        #print(statement)
        IR = Instruction(statement)
        IR_code.append(IR)
        ex = 0
        if IR.operation in leader_instructions:
            if IR.operation != "label"  and IR.operation != "func":
                ex += 1

            leader.add(j-1+ex)
        j+=1

    leader.add(len(IR_code))

    return (sorted(leader), IR_code)

def next_use(leader, IR_code):

    generator = CodeGenerator()
    for b_start in range(len(leader) -  1):
        # iterate through all basic blocks
        basic_block = IR_code[leader[b_start] :leader[b_start + 1] ]
        # for x in basic_block:
            # print(x.inp1, x.out)
        # for instr in basic_block:
        #     if instr.instr_type == "begin_func" and instr.table != None:
        #         symbol_table = instr.table

        j = leader[b_start + 1] - 1
        for instr in reversed(basic_block):
            for sym in [instr.out,instr.inp1,instr.inp2]:
                if is_valid_sym(sym):
                    instr.inst_info['next_use'][sym] = copy.deepcopy(symbol_table[sym].next_use)
            for sym in [instr.out,instr.inp1,instr.inp2]:
                if is_valid_sym(sym):
                    instr.inst_info['live'][sym] = copy.deepcopy(symbol_table[sym].live)
            if is_valid_sym(instr.out) and instr.array_index_o == None:
                symbol_table[instr.out].live = False
                symbol_table[instr.out].next_use = None

            if is_valid_sym(instr.inp1):
                symbol_table[instr.inp1].live = True
                symbol_table[instr.inp1].next_use = j

            if is_valid_sym(instr.inp2):
                symbol_table[instr.inp2].live = True
                symbol_table[instr.inp2].next_use = j

            if instr.array_index_o and is_valid_sym(instr.array_index_o):
                symbol_table[instr.array_index_o].live = True
                symbol_table[instr.array_index_o].next_use = j

            if instr.array_index_i1 and is_valid_sym(instr.array_index_i1):
                symbol_table[instr.array_index_i1].live = True
                symbol_table[instr.array_index_i1].next_use = j
            j-=1

        for instr in basic_block:
            # print(instr)
            generator.gen_code(instr)
        # save_caller_context()
        reset_live_and_next_use()


if __name__ == "__main__":
    # parser_main()
    leader, IR_code = read_three_address_code(sys.argv[1])
    # print(leader)
    # print(len(IR_code))
    generator.gen_data_section()
    generator.gen_start_template()
    next_use(leader, IR_code)
    # for key in symbol_table.keys():
    #     print(key,symbol_table[key].isArg)