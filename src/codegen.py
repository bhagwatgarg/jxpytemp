import sys
import copy
from math import log
from get_reg import *
from utilities import *
import global_vars as g

class CodeGenerator:

    # def gen_data_section(self):
    #     print("extern printf\n")
    #     print("extern scanf\n")
    #     print("extern malloc\n")
    #     print("section\t.data\n")
    #     print("print_int:\tdb\t\"%d\",10,0")
    #     print("print_char:\tdb\t\"%c\",0")
    #     print("scan_int:\tdb\t\"%d\",0")
    #     for temp_var in g.temp_var_set:
    #         print(temp_var + "\tdd\t0")
    #     # for symbol in g.symbol_table.keys():
    #         # if g.symbol_table[symbol].array_size != None:
    #             # print(str(symbol) + "\ttimes\t" + str(g.symbol_table[symbol].array_size) + "\tdd\t0")
    #         # else:
    #             # print(str(symbol) + "\tdd\t0")

    # def gen_start_template(self):
    #     print()
    #     print("section .text")
    #     print("\tglobal main")

    # def op_print_int(self, instr):
    #     loc = get_location(instr.inp1)
    #     save_context()
    #     if loc not in reg_descriptor.keys():
    #         print("\tmov eax, " + loc)
    #         loc = "eax"
    #     print("\tpush ebp")
    #     print("\tmov ebp,esp")
    #     print("\tpush dword " + str(loc))
    #     print("\tpush dword print_int")
    #     print("\tcall printf")
    #     print("\tadd esp, 8")
    #     print("\tmov esp, ebp")
    #     print("\tpop ebp")

    # def op_print_char(self, instr):
    #     loc = get_location(instr.inp1)
    #     save_context()
    #     if loc not in reg_descriptor.keys():
    #         print("\tmov eax, " + loc)
    #         loc = "eax"
    #     print("\tpush ebp")
    #     print("\tmov ebp,esp")
    #     print("\tpush dword " + str(loc))
    #     print("\tpush dword print_char")
    #     print("\tcall printf")
    #     print("\tadd esp, 8")
    #     print("\tmov esp, ebp")
    #     print("\tpop ebp")

    # def op_scan_int(self, instr):
    #     save_context()
    #     loc = get_location(instr.out)
    #     print("\tlea eax, " + loc)
    #     print("\tpush ebp")
    #     print("\tmov ebp,esp")
    #     print("\tpush eax")
    #     print("\tpush scan_int")
    #     print("\tcall scanf")
    #     print("\tadd esp, 8")
    #     print("\tmov esp, ebp")
    #     print("\tpop ebp")

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

        if is_valid_number(instr.inp1) and is_valid_number(instr.inp2):
             inp1 = int(instr.inp1)
             inp2 = int(instr.inp2)

        R1, flag = get_reg(instr)
        if flag:
            print("\tmov"+ ' '+ R1 + ", " + get_location(instr.inp1))
        R2 = get_location(instr.inp2)
        print("\t"+op+ ' ' + R1 + ", " + R2)
        update_reg_descriptors(R1,instr.out)
        free_regs(instr)
    
    def op_fbinary(self,instr,op):

        if is_valid_number(instr.inp1) and is_valid_number(instr.inp2):
             inp1 = float(instr.inp1)
             inp2 = float(instr.inp2)

        R1, flag = get_reg(instr,is_float=True)
        if flag:
            print("\tmov"+ ' '+ R1 + ", " + get_location(instr.inp1))
        R2 = get_location(instr.inp2)
        print("\t"+op+ ' ' + R1 + ", " + R2)
        update_reg_descriptors(R1,instr.out)
        free_regs(instr)


    def op_add(self, instr):

        self.op_binary(instr,'add')


    def op_sub(self, instr):
        
        self.op_binary(instr,'sub')


    def op_mult(self, instr):

        if is_valid_number(instr.inp1) and is_valid_number(instr.inp2):
             inp1 = int(instr.inp1)
             inp2 = int(instr.inp2)

        R1, flag = get_reg(instr)
        if flag:
            print("\tmov "+ R1 + ", " + get_location(instr.inp1))
        # handle cases when inp2 is a power of 2
        bitshift = False        # to avoid multiple operations
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
        update_reg_descriptors(R1, instr.out)
        free_regs(instr)


    def op_div(self, instr):

        if is_valid_number(instr.inp1) and is_valid_number(instr.inp2):
             inp1 = int(instr.inp1)
             inp2 = int(instr.inp2)

        save_reg_contents("eax")
        print("\tmov eax, " + get_location(instr.inp1))
        save_reg_contents("edx")
        if is_valid_number(instr.inp2):
            R1, flag = get_reg(instr,exclude=["eax","edx"])
            print("\tmov " + R1 + ", " + get_location(instr.inp2))
            print("\tcdq")
            print("\tidiv " + R1)
        else:
            print("\tcdq")
            print("\tidiv dword " + get_location(instr.inp2))
        update_reg_descriptors("eax", instr.out)
        free_regs(instr)
    
    def op_fadd(self,instr):
        self.op_fbinary(instr,'addss')

    def real_sub(self,quad):
        self.op_fbinary(quad,'subss')

    def real_mul(self,quad):
        self.op_fbinary(instr, 'mulss')

    def real_div(self,quad):
        self.op_fbinary(instr, 'divss')



    def op_modulo(self, instr):
        optimized = self.optimize_if_possible(instr.out, instr.inp1, instr.inp2, instr.operation)
        if optimized:
            return
        save_reg_contents("eax")
        print("\tmov eax, " + get_location(instr.inp1))
        save_reg_contents("edx")
        if is_valid_number(instr.inp2):
            R1, flag = get_reg(instr,exclude=["eax","edx"])
            print("\tmov " + R1 + ", " + get_location(instr.inp2))
            print("\tcdq")
            print("\tidiv " + R1)
        else:
            print("\tcdq")
            print("\tidiv dword" + get_location(instr.inp2))

        update_reg_descriptors("edx", instr.out)
        free_regs(instr)


    def op_lshift(self, instr):
        optimized = self.optimize_if_possible(instr.out, instr.inp1, instr.inp2, instr.operation)
        if optimized:
            return
        R1, flag = get_reg(instr)
        if flag:
            print("\tmov "+ R1 + ", " + get_location(instr.inp1))
        R2 = None
        if is_valid_number(instr.inp2):
            R2 = instr.inp2
        else:
            R2 = get_location(instr.inp2)
        print("\tshl " + R1 + ", " + R2)
        update_reg_descriptors(R1, instr.out)
        free_regs(instr)


    def op_rshift(self, instr):
        optimized = self.optimize_if_possible(instr.out, instr.inp1, instr.inp2, instr.operation)
        if optimized:
            return
        R1, flag = get_reg(instr)
        if flag:
            print("\tmov "+ R1 + ", " + get_location(instr.inp1))
        R2 = None
        if is_valid_number(instr.inp2):
            R2 = instr.inp2
        else:
            R2 = get_location(instr.inp2)
        print("\tshr " + R1 + ", " + R2)
        update_reg_descriptors(R1, instr.out)
        free_regs(instr)


    def op_assign(self, instr):
        if instr.array_index_i1 == None and instr.array_index_o == None and is_valid_number(instr.inp1):
            R1, flag = get_reg(instr, compulsory=False)
            print("\tmov " + R1 + ", " + get_location(instr.inp1))
            if R1 in reg_descriptor.keys():
                update_reg_descriptors(R1, instr.out)

        elif instr.array_index_i1 == None and instr.array_index_o == None:
            if len(g.symbol_table[instr.inp1].address_descriptor_reg) == 0:
                R1, flag = get_reg(instr)
                print("\tmov " + R1 +", " + get_location(instr.inp1))
                update_reg_descriptors(R1,instr.inp1)

            if len(g.symbol_table[instr.inp1].address_descriptor_reg):
                for regs in g.symbol_table[instr.out].address_descriptor_reg:
                    reg_descriptor[regs].remove(instr.out)
                g.symbol_table[instr.out].address_descriptor_reg.clear()
                g.symbol_table[instr.out].address_descriptor_reg = copy.deepcopy(g.symbol_table[instr.inp1].address_descriptor_reg)

                for reg in g.symbol_table[instr.out].address_descriptor_reg:
                    reg_descriptor[reg].add(instr.out)

                free_regs(instr)

        elif instr.array_index_i1 != None:
            # assert len(g.symbol_table[instr.inp1].address_descriptor_reg) == 0
            R1, flag = get_reg(instr)
            print("\tmov " + R1 + ", " + get_location(instr.array_index_i1))
            print("\tshl " + R1 + ", 2")
            print("\tadd " + R1 + ", " + get_location(instr.inp1))
            print("\tmov " + R1 + ", [" + R1 + "]")
            update_reg_descriptors(R1, instr.out)

        else:
            index = instr.array_index_o
            loc_arr = get_location(instr.out)
            if loc_arr in reg_descriptor.keys():
                R1 = None
                if is_valid_sym(index):
                    if len(g.symbol_table[index].address_descriptor_reg) == 0:
                        R1, _ = get_reg(instr, exclude=[loc_arr])
                        print("\tmov " + R1 + ", " + get_location(index))
                        update_reg_descriptors(R1, index)
                    else:
                        R1 = get_location(index)

                    inp_reg = R1
                    if index != instr.inp1:
                        inp_reg, flag = get_reg(instr, exclude=[R1, loc_arr])
                        if flag:
                            print("\tmov " + inp_reg + ", " + get_location(instr.inp1))
                            update_reg_descriptors(inp_reg,instr.inp1)
                    print("\tmov [" + loc_arr + "," + R1 + "*4], " + inp_reg)
                else:
                    index = 4 * int(index)
                    inp_reg, flag = get_reg(instr)
                    if flag:
                        print("\tmov " + inp_reg + ", " + get_location(instr.inp1))
                        update_reg_descriptors(inp_reg,instr.inp1)
                    print("\tmov [" + loc_arr + "+" + str(index) + "], " + inp_reg)
            else:
                loc_inp1 = get_location(instr.inp1)
                R1, _ = get_reg(instr, exclude=[loc_inp1])
                print("\tmov " + R1 + ", " + get_location(index))
                print("\tshl " + R1 + ", 2")
                print("\tadd " + R1 + ", " + loc_arr)
                if loc_inp1 in reg_descriptor.keys():
                    print("\tmov [" + R1 + "], " + loc_inp1)
                else:
                    inp_reg, _ = get_reg(instr, exclude=[R1])
                    print("\tmov " + inp_reg + ", " + loc_inp1)
                    update_reg_descriptors(inp_reg, instr.inp1)
                    print("\tmov [" + R1 + "], " + inp_reg)

    def op_logical(self, instr):
        # TODO: logical &&, ||
        R1, flag = get_reg(instr)
        if flag:
            print("\tmov "+ R1 + ", " + get_location(instr.inp1))
        R2 = get_location(instr.inp2)
        def log_op(x):
            return {
                    "&" : "and ",
                    "|" : "or ",
                    "^" : "xor ",
                    # remove the following 2 lines after TODO
                    "&&": "and ",
                    "||": "or ",
            }[x]
        if (instr.operation != "~" and instr.operation != "!"):
            print("\t" + log_op(instr.operation) + R1 + ", " + R2)
        else:
            print("\tnot " + R1)
        update_reg_descriptors(R1,instr.out)
        free_regs(instr)

    def op_unary(self, instr):
        R1, flag = get_reg(instr,compulsory=False)
        if R1 not in reg_descriptor.keys():
            R1 = "dword " + R1
        if flag:
            print("\tmov "+ R1 + ", " + get_location(instr.inp1))
        if instr.operation == "!" or instr.operation == "~":
            print("\tnot "+ R1)
        elif instr.operation == "++":
            print("\tinc "+ R1)
        elif instr.operation == "--":
            print("\tdec "+ R1)
        if R1 in reg_descriptor.keys():
            update_reg_descriptors(R1,instr.out)
        free_regs(instr)

    def op_ifgoto(self, instr):
        inp1 = instr.inp1
        inp2 = instr.inp2
        out = None
        jmp_label = None
        if instr.jmp_to_line != None:
            jmp_label = "line_no_" + str(instr.jmp_to_line)
        else:
            jmp_label = "func_" + instr.jmp_to_label

        operator = instr.operation
        if is_valid_number(instr.inp1) and is_valid_number(instr.inp2):
            save_context()
            if operator == "geq":
                if inp1 >= inp2:
                    print("\tjmp " + jmp_label)
            elif operator == "gt":
                if inp1 > inp2:
                    print("\tjmp " + jmp_label)
            elif operator == "leq":
                if inp1 <= inp2:
                    print("\tjmp " + jmp_label)
            elif operator == "lt":
                if inp1 < inp2:
                    print("\tjmp " + jmp_label)
            elif operator == "eq":
                if inp1 == inp2:
                    print("\tjmp " + jmp_label)
            elif operator == "neq":
                if inp1 != inp2:
                    print("\tjmp " + jmp_label)
            return

        R1 = get_location(inp1)
        R2 = get_location(inp2)
        if R1 in reg_descriptor.keys():
            print("\tcmp " + R1 + ", " + R2)
        elif R2 in reg_descriptor.keys():
            print("\tcmp " + R1 + ", " + R2)
        else:
            instr.out = inp1
            instr.inp1 = None
            R, flag = get_reg(instr)
            print("\tmov " + R + ", " + R1)
            update_reg_descriptors(R,inp1)
            print("\tcmp " + R + ", " + R2)

        save_context()
        if operator == "geq":
            print("\tjge " + jmp_label)
        elif operator == "gt":
            print("\tjg " + jmp_label)
        elif operator == "leq":
            print("\tjle " + jmp_label)
        elif operator == "lt":
            print("\tjl " + jmp_label)
        elif operator == "eq":
            print("\tje " + jmp_label)
        elif operator == "neq":
            print("\tjne " + jmp_label)

        free_regs(instr)

    def op_goto(self, instr):
        save_context()
        jmp_label = None
        if instr.jmp_to_line != None:
            jmp_label = "line_no_" + str(instr.jmp_to_line)
        else:
            jmp_label = "func_" + instr.jmp_to_label
        print("\tjmp " + jmp_label)

    def op_label(self, instr):
        save_context()
        print("func_" + instr.label_name + ":")

    def op_param(self, instr):
        print("\tpush dword " + get_location(instr.inp1))

    def op_call_function(self, instr):
        save_context()
        print("\tcall func_" + instr.jmp_to_label)
        print("\tadd esp, " + str(4 * int(instr.inp1)))
        if instr.out != None:
            update_reg_descriptors("eax",instr.out)

    def op_return(self, instr):
        if instr.inp1 != None:
            loc = get_location(instr.inp1)
            save_reg_contents("eax")
            if loc != "eax":
                print("\tmov eax, " + loc)
            save_context(exclude=["eax"])
        else:
            save_context()
        print("\tmov esp, ebp")
        print("\tpop ebp")
        print("\tret")

    def op_stack_alloc(self, instr):
        if instr.label_name == "main":
            print("main:")
        print("func__l" + instr.label_name + ":")
        g.counter = 0
        for i in g.symbol_table.keys():
            if not is_temp_var(i) and i not in instr.arg_set:
                g.counter += 1
                g.symbol_table[i].address_descriptor_mem.add(-4 * g.counter)
        for i, arg in enumerate(reversed(instr.arg_set)):
            g.symbol_table[arg].address_descriptor_mem.add(4 * i + 8)

        print("\tpush ebp")
        print("\tmov ebp, esp")
        print("\tsub esp, " + str(4*g.counter))

    def op_array_decl(self, instr):
        loc = get_location(instr.array_index_i1)
        save_context()
        if loc not in reg_descriptor.keys():
            print("\tmov eax," + loc)
            loc = "eax"
        print("\tpush ebp")
        print("\tmov ebp, esp")
        print("\tshl " + loc + ", 2")
        print("\tpush " + loc)
        print("\tcall malloc")
        print("\tadd esp, 4")
        print("\tmov esp, ebp")
        print("\tpop ebp")
        update_reg_descriptors("eax", instr.inp1)

    def gen_code(self, instr):
        '''
        Main function which calls other utility functions
        according to instruction type
        '''
        instr_type = instr.instr_type
        if instr.label_to_be_added == True:
            save_context()
            print("line_no_" + str(instr.line_no) + ":")

        if instr_type == "arithmetic":
            if instr.operation == "+":
                self.op_add(instr)
            elif instr.operation == "-":
                self.op_sub(instr)
            elif instr.operation == "*":
                self.op_mult(instr)
            elif instr.operation == "/":
                self.op_div(instr)
            elif instr.operation == "%":
                self.op_modulo(instr)
            elif instr.operation == "<<":
                self.op_lshift(instr)
            elif instr.operation == ">>":
                self.op_rshift(instr)

        elif instr_type == "logical":
            self.op_logical(instr)

        elif instr_type == "assignment":
            self.op_assign(instr)

        elif instr_type == "ifgoto":
            self.op_ifgoto(instr)

        elif instr_type == "goto":
            self.op_goto(instr)

        elif instr_type == "return":
            self.op_return(instr)

        elif instr_type == "label":
            self.op_label(instr)

        elif instr_type == "param":
            self.op_param(instr)

        elif instr_type == "func_call":
            self.op_call_function(instr)

        elif instr_type == "print_int":
            self.op_print_int(instr)

        elif instr_type == "print_char":
            self.op_print_char(instr)

        elif instr_type == "scan_int":
            self.op_scan_int(instr)

        elif instr_type == "unary":
            self.op_unary(instr)

        elif instr_type == "begin_func":
            self.op_stack_alloc(instr)
            # for sym, symentry in g.symbol_table.items():
                # print(sym, symentry.address_descriptor_mem)

        elif instr_type == "array_declaration":
            self.op_array_decl(instr)


###################################global generator############################
generator = CodeGenerator()
###################################global generator############################

def next_use(leader, IR_code):
    '''
    This function determines liveness and next
    use information for each statement in basic block by
    performing a backward pass
    Then, it generates assembly code for each basic block
    by making a forward pass
    Finally, it saves all register contents into memory and
    resets the liveness and next use info in symbol table.
    '''
    generator = CodeGenerator()
    for b_start in range(len(leader) -  1):
        # iterate through all basic blocks
        basic_block = IR_code[leader[b_start] - 1:leader[b_start + 1] - 1]
        # for x in basic_block:
            # print(x.inp1, x.out)
        for instr in basic_block:
            if instr.instr_type == "begin_func" and instr.table != None:
                g.symbol_table = instr.table

        for instr in reversed(basic_block):
            instr.per_inst_next_use = copy.deepcopy(g.symbol_table)

            if is_valid_sym(instr.out) and instr.array_index_o == None:
                g.symbol_table[instr.out].live = False
                g.symbol_table[instr.out].next_use = None

            if is_valid_sym(instr.inp1):
                g.symbol_table[instr.inp1].live = True
                g.symbol_table[instr.inp1].next_use = instr.line_no

            if is_valid_sym(instr.inp2):
                g.symbol_table[instr.inp2].live = True
                g.symbol_table[instr.inp2].next_use = instr.line_no

            if instr.array_index_o and is_valid_sym(instr.array_index_o):
                g.symbol_table[instr.array_index_o].live = True
                g.symbol_table[instr.array_index_o].next_use = instr.line_no

            if instr.array_index_i1 and is_valid_sym(instr.array_index_i1):
                g.symbol_table[instr.array_index_i1].live = True
                g.symbol_table[instr.array_index_i1].next_use = instr.line_no

        for instr in basic_block:
            generator.gen_code(instr)
        # save_context()
        reset_live_and_next_use()


if __name__ == "__main__":
    # parser_main()
    leader, IR_code = read_three_address_code(sys.argv[1])
    generator.gen_data_section()
    generator.gen_start_template()
    next_use(leader, IR_code)