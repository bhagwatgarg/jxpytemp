from new_sym_table import ScopeTable

global ST
ST = ScopeTable()

class TAC:

    def __init__(self):
        self.l_count = 0
        self.code = []

    def newLabel(self):
        self.l_count += 1
        return "l" + str(self.l_count - 1)

    def emit(self, lhs, mhs, rhs, op):
        self.code.append([lhs, str(mhs), str(rhs), op])

    def backpatch(self, lst, label):
        for i in lst:
            self.code[i][3] = label
