import pandas as pd

widths = {'int':4, 'float':8, 'short':4, 'long':8, 'double':8, 'char':1}

class ScopeTable:
    def __init__(self): #list of all symbol tables in program
        
        self.label_counter = 0
        self.label_prefix = '_n'
        self.temp_var_counter = 0
        self.key_counter = 0
        self.curr_scope = 'compilation_unit'
        self.curr_sym_table = SymbolTable(self.curr_scope, parent=None)
        self.scope_and_table_map = dict()
        self.scope_and_table_map[self.curr_scope] = self.curr_sym_table

    def create_new_table(self, new_label, scope_type = None): #If func_name is not provided, use custom label
        label = new_label
        # if scope_type == "func":
        #     label = new_label + '_' + self.scope_and_table_map[self.curr_scope].scope
        new_sym_table = SymbolTable(label, self.curr_scope, self.curr_sym_table, scope_type)
        self.curr_scope = label
        self.curr_sym_table = new_sym_table
        self.key_counter += 1
        self.scope_and_table_map[self.curr_scope] = new_sym_table

    def end_scope(self):
        if self.scope_and_table_map[self.curr_scope].scope_type == "class": 
            widths[self.curr_scope] = self.scope_and_table_map[self.curr_scope].width
        self.curr_scope = self.scope_and_table_map[self.curr_scope].parent
        self.curr_sym_table=self.curr_sym_table.parent_table

    def lookup(self, symbol, is_func=False):
        return self._lookup(symbol, is_func, self.curr_sym_table)
    
    def _lookup(self, symbol, is_func=False, table=None):
        if table==None: return None
        if symbol in table.functions and is_func:
            return table.functions[symbol]
            
        elif symbol in table.symbols and not is_func:
            return table.symbols[symbol]
        return self._lookup(symbol, is_func, table.parent_table)

    def make_label(self):
        self.label_counter += 1
        return  self.label_prefix

    def get_parent_scope(self):
        return self.scope_and_table_map[self.curr_scope].parent

    def get_temp_var(self):
        self.temp_var_counter += 1
        return str(self.temp_var_counter)

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
            self.scope_and_table_map[scope].add_function(idName, idType, args, modifiers=modifiers, return_type=return_type)

    def print_curr_scope(self):
        self.curr_sym_table.print_table()
    def print_scope_table(self):
        for key, val in self.scope_and_table_map.items():
            # if val.scope_type == "func":
                val.print_table()


class SymbolTable:
    def __init__(self, scope, parent, parent_table=None, scope_type=None):
        '''
        Symbol table class for each block in program
        '''
        self.scope = scope
        self.parent = parent
        self.symbols = dict()
        self.functions = dict()
        self.blocks = set()
        self.parent_table=parent_table
        self.scope_type = scope_type

        self.offset = 0
        self.width = 0


    def add_symbol(self, idName, idType, is_array=False, dims=None, arr_size=None, modifiers=[]):
        if idName in self.symbols.keys():
            raise Exception('Variable %s redeclared, check your program' %(idName))

        # add the ID to symbols dict if not present earlier
        if idName in self.symbols.keys():
            raise Exception('Variable %s redeclared, check your program' % (idName))
        
        width = 0
        offset = self.offset
        try:
            if idType in widths.keys():
                width = widths[idType]
            elif idType == 'class' and idName in widths.keys():
                width = widths[idName] 
        except:
            pass
     
        if is_array:
            for i in arr_size:
                try:
                    width *= int(i)
                except ValueError:
                    pass

        self.offset = self.width
        self.width += width

        if idType == 'class' and idName not in widths.keys():
            width = 8
            self.offset += 8

        self.symbols[idName] = {
            'type' : idType,
            'is_array' : is_array,
            'dims' : dims,
            'arr_size' : arr_size,
            'modifiers': modifiers,
            'width' : width,
            'offset' : offset,
        }

    def add_function(self, func_name, type=None, params=None, modifiers=[], return_type=None):
        if func_name in self.functions.keys():
            raise Exception('Function %s redeclared, check your program' % (func_name))

        self.offset = self.width
        self.width += 8
        
        self.functions[func_name] = {
            'n_params': len(params),
            'params': params,
            'return_type': return_type,
            'modifiers': modifiers,
            'type' : 'func',
            'width' : 8,
            'offset' : self.offset,
        }

    def add_block(self, block_name):
        self.blocks.add(block_name)

    def print_table(self):

        # store = []

        # for key, val in self.symbols.items():
        #     store.append([key])
        #     for k, v in val.items():
        #         store[-1].append(v)

        # for key, val in self.functions.items():
        #     store.append([key])
        #     for k, v in val.items():
        #         store[-1].append(v)

        # df = pd.DataFrame(store, columns = ['name', 'type', 'is_array', 'dims', 'arr_size', 'modifiers', 'width', 'offset'])

        # df.to_csv(f"{self.parent}_{self.scope}.csv", index = False)

        print("Parent: %s" %(self.parent))
        print("Scope: %s \nSymbols:" %(self.scope))
        for key, val in self.symbols.items():
            print(key,val)
        print("Functions:")
        for key, val in self.functions.items():
            print(key,val)
        print("*************************")