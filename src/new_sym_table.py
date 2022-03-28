class SymbolTableEntry:
    def __init__(self):
        # self.value = None
        self.live = True
        self.next_use = None
        self.array_size = None
        self.address_descriptor_mem = set()
        self.address_descriptor_reg = set()


class ScopeTable:
    def __init__(self): #list of all symbol tables in program
        
        self.label_counter = 0
        self.curr_scope = 'start'
        self.label_prefix = '_l'
        self.temp_var_counter = 0
        self.curr_sym_table = SymbolTable(self.curr_scope, parent=None)
        self.scope_and_table_map = dict()
        self.scope_and_table_map[self.curr_scope] = self.curr_sym_table

    def create_new_table(self, new_label): #If func_name is not provided, use custom label
        new_sym_table = SymbolTable(new_label, self.curr_scope)
        self.curr_scope = new_label
        self.scope_and_table_map[self.curr_scope] = new_sym_table

    def end_scope(self):
        self.curr_scope = self.scope_and_table_map[self.curr_scope].parent

    def lookup(self, symbol, is_func=False):
        scope = self.curr_scope

        while scope != None:
            if symbol in self.scope_and_table_map[scope].functions and is_func:
                return self.scope_and_table_map[scope].functions[symbol]
                
            elif symbol in self.scope_and_table_map[scope].symbols and not is_func:
                return self.scope_and_table_map[scope].symbols[symbol]
            scope = self.scope_and_table_map[scope].parent

        return None

    def make_label(self):
        self.label_counter += 1
        return str(self.label_counter) + self.label_prefix 

    def get_parent_scope(self):
        return self.scope_and_table_map[self.curr_scope].parent

    def get_temp_var(self):
        prefix = "_"
        self.temp_var_counter += 1
        return prefix + str(self.temp_var_counter)

    def insert_in_sym_table(self, idName, idType, is_func=False, args=None, is_array=False, dims=None, arr_size=None, scope=None, modifiers=[], return_type=None):
        '''
        Universal function to insert any symbol into current symbol table
        Returns a string representing the new scope name if a new block is
        about to start; otherwise returns None
        '''
        if scope == None:
            scope = self.curr_scope
        if not is_func:
            self.scope_and_table_map[scope].add_symbol(idName, idType, is_array, dims, arr_size, modifiers=modifiers)
            return None
        else:
            self.scope_and_table_map[scope].add_function(
                idName, idType, args, modifiers=modifiers, return_type=return_type)

    def print_scope_table(self):
        for key, val in self.scope_and_table_map.items():
            val.print_table()


class SymbolTable:
    def __init__(self, scope, parent):
        '''
        Symbol table class for each block in program
        '''
        self.scope = scope + "_" + str(parent)
        self.parent = parent
        self.symbols = dict()
        self.functions = dict()
        self.blocks = set()

        self.stack_size = 0
        self.table_offset = 0


    def add_symbol(self, idName, idType, is_array=False, dims=None, arr_size=None, modifiers=[]):
        if idName in self.symbols.keys():
            raise Exception('Variable %s redeclared, check your program' %(idName))

        # add the ID to symbols dict if not present earlier
        if idName in self.symbols.keys():
            raise Exception(
                'Variable %s redeclared, check your program' % (idName))
        self.symbols[idName] = {
            'type' : idType,
            'is_array' : is_array,
            'dims' : dims,
            'arr_size' : arr_size,
            'modifiers': modifiers,
        }

        self.stack_size += 1

    def add_function(self, func_name, type=None, params=None, modifiers=[], return_type=None):
        if func_name in self.functions.keys():
            raise Exception(
                'Function %s redeclared, check your program' % (func_name))

        self.functions[func_name] = {
            'n_params': len(params),
            'params': params,
            'return_type': return_type,
            'modifiers': modifiers,
            'type' : 'func'

        }

    def add_block(self, block_name):
        self.blocks.add(block_name)

    def print_table(self):
        print("Parent: %s" % (self.parent))
        print("Scope: %s \nSymbols:" % (self.scope))
        for key, val in self.symbols.items():
            print(key, val)
        print("Functions:")
        for key, val in self.functions.items():
            print(key, val)
        print("*************************")
