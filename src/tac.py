from new_sym_table import ScopeTable

class TAC:
    def __init__(self):
        self.code_list = []
        self.label_count = 0
        self.prefix = ScopeTable().label_prefix

    def emit(self, dest, src1, src2, op):
        self.code_list.append([dest, src1, src2, op])

    def error(self, msg):
        pass

    def generate(self):
        for i in range(len(self.code_list)):
            instr = self.code_list[i]
            if instr[3] in ['*', '/', '%', '+', '-', '>>', '<<', '&', '|', '^']:
                if instr[2] == '1' and instr[3] in ['+','-']:
                    print(str(i + 1) + ", " + str(instr[3])*2  + " , " + str(instr[1]) + ", " + str(instr[1]))
                else:
                    print(str(i + 1) + ", " + str(instr[3]) +", " + str(instr[0]) + ", " + str(instr[1]) + ", " + str(instr[2]))
            elif instr[3] == '=':
                print(str(i + 1) + ", = , " + str(instr[0]) + ", " + str(instr[1]))
            elif instr[0] == 'declare':
                print("Currently unimplemented: DECLARATION")
            elif instr[3] in ['&&', '||', 'xor']:
                print(str(i + 1) + ", " + str(instr[3]) +", " + str(instr[0]) + ", " + str(instr[1]) + ", " + str(instr[2]))
            elif instr[0] == 'goto':
                print(str(i + 1) + ", " + str(instr[0]) + ", " + str(instr[1]))
            elif instr[0] == 'ifgoto':
                print(str(i + 1) + ", " + str(instr[0]) + ", " + str(instr[1]) + ", " + str(instr[2]) + ", " + str(instr[3]))
            elif instr[0] == 'ret':
                print(str(i + 1) + ", " + str(instr[0]) + ", " + str(instr[1]))
            elif instr[0] == 'label':
                print(str(i + 1) + ", label, " + str(instr[1]))
            elif instr[0] == 'func':
                print(str(i + 1) + ", label, " + self.prefix + str(instr[1]))
            elif instr[0] == 'call':
                print(str(i + 1) + ", call, " + self.prefix + str(instr[1]) + ", " + str(instr[2]))
            elif instr[0] == 'param':
                print(str(i + 1) + ", param, " + str(instr[1]))
            elif instr[0] == 'print':
                print(str(i + 1) + ", print, " + str(instr[1]))
