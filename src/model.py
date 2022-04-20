from tac import *
# widths = {'int': 4, 'float': 8, 'short': 4, 'long': 8, 'double': 8, 'char': 1}
primitives = ['int', 'float', 'bool', 'char', 'long', 'double']
count = -1

tac = TAC()

priorities = {
    'double': 5,
    'float': 4,
    'long': 3,
    'int': 2,
    'char': 1,
    'bool': 0
}


def highest_prior(lhs_type, rhs_type):
    if priorities[lhs_type] > priorities[rhs_type]:
        return lhs_type
    else:
        return rhs_type


# handles emit for all kinds of binary operators


def int_or_real(type):  # given a type as input, returns its type
    if type in ['int', 'long']:
        return 'int'
    elif type in ['float', 'double']:
        return 'float'
    elif type in ['char']:
        return 'char'


# def get_func_name(id, params):
#     idName = id + "$" + ST.curr_scope
#     if params == None:
#         params = []
#     for i in params:
#         idName += "$" + i.type
#     return idName
def get_func_name(id, params):
    idName = id + "$" + ST.curr_scope
    if params == None:
        params = []
    for i in params:
        if isinstance(i.type, Type):
            idName += "$" + i.type.name
        else:
            idName += "$" + i.type
    return idName


class BaseClass(object):
    '''
    A BaseClass is the base class for all elements that occur in the program
    '''

    def __init__(self):
        super(BaseClass, self).__init__()
        self._fields = []
        self.symb = {}
        self.methods = {}
        self.classes = {}
        self.parent = None
        self.scope = None

    def __repr__(self):
        equals = ["{0}={1!r}".format(k, getattr(self, k))
                  for k in self._fields]
        # equals.append(f"width={self.width}")
        args = ", ".join(equals)
        return "{0}({1})".format(self.__class__.__name__, args)

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self == other

    def itr(self, elem, parent, payload=None, given_name=None):

        global count
        count += 1
        elem.parent = parent

        if isinstance(payload, dict):
            for key, value in payload.items():
                elem.symb[key] = value
            payload = None

        body = elem
        if isinstance(elem, CompilationUnit):
            body = elem.type_declarations
            elem.scope = "compilation_unit"
        elif isinstance(elem, ScopeField):
            if 'name' in elem._fields:
                elem.scope = elem.name
            else:
                elem.scope = elem.__class__.__name__

            if isinstance(elem, IfThenElse):
                if payload == True:
                    body = elem.if_true
                else:
                    body = elem.if_false
                payload = None
            elif 'body' in elem._fields:
                body = elem.body
            elif 'block' in elem._fields:
                body = elem.block
        elif isinstance(elem, Switch):
            body = elem.switch_cases
            for i in body:
                elem.itr(i, elem.parent, None,
                         given_name=f"switch_case_{i.cases[0].value}")
            return

        if given_name != None:
            elem.scope = given_name

        elem.scope += "_" + str(count)

        if isinstance(body, Block):
            body = body.statements

        if isinstance(elem, For):
            body = [elem.init] + body

        if not isinstance(body, list):
            return

        for i in body:
            if isinstance(i, MethodDeclaration) or isinstance(i, ConstructorDeclaration):
                parameters = {}

                for j in i.parameters:
                    type = ""
                    is_array = False
                    dims = 0
                    arr_size = []
                    if isinstance(j.type, Type):
                        if isinstance(j.type.name, Name):
                            type = j.type.name.value
                        else:
                            type = j.type.name
                        if j.type.dimensions > 0:
                            is_array = True
                            dims = j.type.dimensions
                    elif isinstance(j.type, Name):
                        type = j.type.value
                    else:
                        type = j.type
                    parameters[j.variable.name] = {
                        'type': type, 'is_array': is_array, 'dimensions': dims, 'arr_size': arr_size}

                elem.methods[i.name] = {'n_parameters': len(
                    i.parameters), 'parameters': parameters, 'return_type': i.return_type}

                payload = parameters

            elif isinstance(i, ClassDeclaration):
                elem.classes[i.name] = {}

            elif isinstance(i, VariableDeclaration) or isinstance(i, FieldDeclaration):
                type = ""
                is_array = False
                dims = 0
                arr_size = []
                if isinstance(i.type, Type):
                    if isinstance(i.type.name, Name):
                        type = i.type.name.value
                    else:
                        type = i.type.name
                    if i.type.dimensions > 0:
                        is_array = True
                        dims = i.type.dimensions
                else:
                    if isinstance(i.type, Name):
                        type = i.type.value
                    else:
                        type = i.type

                for j in i.variable_declarators:
                    if isinstance(j, VariableDeclarator):
                        name = j.variable.name
                        if dims == 0:
                            dims = j.variable.dimensions
                        if isinstance(j.initializer, ArrayCreation):
                            is_array = True
                            for k in j.initializer.dimensions:
                                arr_size.append(k.value)

                    elem.symb[name] = {
                        'type': type, 'is_array': is_array, 'dimensions': dims, 'arr_size': arr_size}

            if isinstance(i, ScopeField):
                if isinstance(i, IfThenElse):
                    elem.itr(i, elem, True, "if")
                    temp = i
                    ct = 0
                    while isinstance(temp.if_false, IfThenElse):
                        elem.itr(temp.if_false, elem, True, f"else_if_{ct+1}")
                        ct += 1
                        temp = temp.if_false
                    if temp.if_false != None:
                        elem.itr(temp.if_false, elem, None, "else")

                else:
                    elem.itr(i, elem, payload)
            elif isinstance(i, Switch):
                elem.itr(i, elem)

        if elem.scope != "compilation_unit_0":
            print("Parent:", elem.parent.scope)
        else:
            print("Parent:", elem.parent)
        print("Scope:", elem.scope)
        print("Classes:", elem.classes)
        print("Methods:", elem.methods)
        print("Symbols:", elem.symb)


class ScopeField(BaseClass):
    pass


class CompilationUnit(BaseClass):

    def __init__(self, package_declaration=None, import_declarations=None, type_declarations=None):
        super(CompilationUnit, self).__init__()
        self._fields = ['package_declaration',
                        'import_declarations', 'type_declarations']
        if import_declarations is None:
            import_declarations = []
        if type_declarations is None:
            type_declarations = []
        self.package_declaration = package_declaration
        self.import_declarations = import_declarations
        self.type_declarations = type_declarations


class PackageDeclaration(BaseClass):

    def __init__(self, name, modifiers=None):
        super(PackageDeclaration, self).__init__()
        self._fields = ['name']
        self.name = name


class ImportDeclaration(BaseClass):

    def __init__(self, name, static=False, on_demand=False):
        super(ImportDeclaration, self).__init__()
        self._fields = ['name', 'static', 'on_demand']
        self.name = name
        self.static = static
        self.on_demand = on_demand


class ClassDeclaration(ScopeField):

    def __init__(self, name, body, modifiers=None, type_parameters=None, extends=None, implements=None):
        super(ClassDeclaration, self).__init__()
        self._fields = ['name', 'body', 'modifiers']
        if modifiers is None:
            modifiers = []
        self.name = name
        self.body = body
        self.modifiers = modifiers

        parent_scope = ST.get_parent_scope()
        ST.insert_in_sym_table(idName=name, idType='class',
                               modifiers=modifiers, scope=parent_scope)
        ST.end_scope()
        # stackbegin.pop()
        # stackend.pop()


class ClassInitializer(ScopeField):

    def __init__(self, block, static=False):
        super(ClassInitializer, self).__init__()
        self._fields = ['block', 'static']
        self.block = block
        self.static = static


class EmptyDeclaration(BaseClass):
    pass


class FieldDeclaration(BaseClass):

    def __init__(self, type, variable_declarators, modifiers=None):
        super(FieldDeclaration, self).__init__()
        self._fields = ['type', 'variable_declarators', 'modifiers']
        if modifiers is None:
            modifiers = []
        self.type = type
        self.variable_declarators = variable_declarators
        self.modifiers = modifiers

        type_ = self.type
        is_array = False
        dims = 0
        arr_size = []
        width = 1

        if isinstance(self.type, Type):
            if isinstance(self.type.name, Name):
                type_ = self.type.name.value
            else:
                type_ = self.type.name
            if self.type.dimensions > 0:
                is_array = True
                type = type.name
                dims = self.type.dimensions
        elif isinstance(self.type, Name):
            type_ = self.type.value

        for j in self.variable_declarators:
            if isinstance(j, VariableDeclarator):
                name = j.variable.name
                if dims == 0:
                    dims = j.variable.dimensions
                if isinstance(j.initializer, ArrayCreation):
                    is_array = True
                    for k in j.initializer.dimensions:
                        arr_size.append(k.value)
                        width *= int(k.value)
                    if j.initializer.type not in primitives:
                        width *= 8
                    else:
                        width *= widths[j.initializer.type ]
                    tac.emit(j.variable.name+'$'+str(ST.curr_scope),
                             width, '', 'declare')
                elif j.initializer:
                    tac.emit(j.variable.name+'$'+str(ST.curr_scope),
                             j.initializer.place, '', '=')

                ST.insert_in_sym_table(idName=name, idType=type_, is_array=is_array,
                                       dims=dims, arr_size=arr_size, modifiers=modifiers)
        self.type = type_
        # if((type_)!=str.ty): print(type_)


class MethodDeclaration(ScopeField):

    def __init__(self, name, modifiers=None, parameters=None, return_type='void', body=None, type_parameters=None, is_declaration=False):
        super(MethodDeclaration, self).__init__()
        self._fields = ['name', 'modifiers', 'parameters',
                        'return_type', 'body', 'type_parameters']
        if modifiers is None:
            modifiers = []
        if parameters is None:
            parameters = []
        self.name = name
        self.modifiers = modifiers
        self.parameters = parameters
        self.return_type = return_type
        self.body = body
        self.type_parameters = type_parameters

        params = []

        for j in self.parameters:
            type = ""
            dims = 0
            is_array = False
            if isinstance(j.type, Type):
                if isinstance(j.type.name, Name):
                    type = j.type.name.value
                else:
                    type = j.type.name
                if j.type.dimensions > 0:
                    is_array = True
                    dims = j.type.dimensions
            elif isinstance(j.type, Name):
                type = j.type.value
            else:
                type = j.type
            params.append({'name': j.variable.name, 'type': type,
                          'is_array': is_array, 'dims': dims})

        parent_scope = ST.get_parent_scope()
        ST.insert_in_sym_table(idName=name, idType='function', is_func=True, args=params,
                               modifiers=modifiers, return_type=return_type, scope=parent_scope, is_declaration=is_declaration)


class ConstructorDeclaration(ScopeField):

    def __init__(self, name, block, modifiers=None, parameters=None):
        super(ConstructorDeclaration, self).__init__()
        self._fields = ['name', 'block', 'modifiers', 'parameters']
        if modifiers is None:
            modifiers = []
        if parameters is None:
            parameters = []
        self.name = name
        self.block = block
        self.modifiers = modifiers
        self.parameters = parameters

        params = []

        for j in self.parameters:
            type = ""
            if isinstance(j.type, Type):
                if isinstance(j.type.name, Name):
                    type = j.type.name.value
                else:
                    type = j.type.name
            elif isinstance(j.type, Name):
                type = j.type.value
            else:
                type = j.type
            params.append({'name': j.variable.name, 'type': type})

        parent_scope = ST.get_parent_scope()
        ST.insert_in_sym_table(name, idType='function', is_func=True,
                               args=params, modifiers=modifiers, scope=parent_scope)
        ST.end_scope()
        # stackbegin.pop()
        # stackend.pop()


class FormalParameter(BaseClass):

    def __init__(self, variable, type):
        super(FormalParameter, self).__init__()
        self._fields = ['variable', 'type']
        self.variable = variable
        self.type = type


class Variable(BaseClass):

    def __init__(self, name, dimensions=0):
        super(Variable, self).__init__()
        self._fields = ['name', 'dimensions']
        self.name = name
        self.dimensions = dimensions


class VariableDeclarator(BaseClass):

    def __init__(self, variable, initializer=None):
        super(VariableDeclarator, self).__init__()
        self._fields = ['variable', 'initializer']
        self.variable = variable
        self.initializer = initializer


class Type(BaseClass):

    def __init__(self, name, dimensions=0):
        super(Type, self).__init__()
        self._fields = ['name', 'dimensions']
        self.name = name
        self.dimensions = dimensions


class Expression(BaseClass):

    def __init__(self):
        super(Expression, self).__init__()
        self._fields = []


class BinaryExpression(Expression):

    def __init__(self, operator, lhs, rhs):
        super(BinaryExpression, self).__init__()
        self._fields = ['operator', 'lhs', 'rhs', 'type',
                        'place', 'place', 'truelist', 'falselist']
        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs
        self.type = None
        self.place = None
        self.truelist = []
        self.falselist = []


class Assignment(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        if lhs.type in ['int', 'double', 'long', 'float', 'char'] and rhs.type in ['int', 'double', 'long', 'float', 'char'] and operator in ['=', '+=', '-=', '*=', '/=', '&=', '|=', '^=', '%=', '<<=', '>>=', '>>>=']:
            self.type = highest_prior(lhs.type, rhs.type)
            self.place = rhs.place
            # if self.type in ['int', 'char', 'long']:
            #     tac.emit(lhs.place, rhs.place, '', operator+'int')
            # elif self.type in ['float', 'double']:
            #     tac.emit(lhs.place, rhs.place, '', operator+'float')
            higher_data_type = int_or_real(highest_prior(lhs.type, rhs.type))
            if (int_or_real(lhs.type) != higher_data_type):
                tmp = ST.get_temp_var()
                tac.emit(tmp, lhs.place, '', int_or_real(lhs.type) +
                         '_' + int_or_real(higher_data_type) + '_' + '=')
                tac.emit(self.place, tmp, rhs.place,
                         higher_data_type+'_'+operator)
            elif (int_or_real(rhs.type) != higher_data_type):
                tmp = ST.get_temp_var()
                tac.emit(tmp, rhs.place, '', int_or_real(rhs.type) +
                         '_' + int_or_real(higher_data_type) + '_' + '=')
                tac.emit(self.place, lhs.place, tmp,
                         higher_data_type + '_' + operator)
            else:
                if lhs.type == 'char':
                    tmp1 = ST.get_temp_var()
                    tac.emit(tmp1, lhs.place, '', int_or_real('char') +
                             '_' + int_or_real('int') + '_' + '=')
                    tmp2 = ST.get_temp_var()
                    tac.emit(tmp2, rhs.place, '', int_or_real('char') +
                             '_' + int_or_real('int') + '_' + '=')
                    tmp3 = ST.get_temp_var()
                    tac.emit(tmp3, tmp1, tmp2, 'int_' + operator)
                    tac.emit(self.place, tmp3, '', int_or_real('int') +
                             '_' + int_or_real('char') + '_' + '=')
                else:
                    tac.emit(self.place, lhs.place, rhs.place,
                             int_or_real(lhs.type) + '_' + operator)
        elif lhs.type != rhs.type:
            print("Type mismatch in assignment.")
            print(lhs, rhs)
        else:  # ask
            # ST.print_scope_table()
            if self.type in ['int', 'char', 'long']:
                tac.emit(lhs.place, rhs.place, '', operator+'int')
            elif self.type in ['float', 'double']:
                tac.emit(lhs.place, rhs.place, '', operator+'float')
            else:
                tac.emit(lhs.place, rhs.place, '', operator+'class')
            # higher_data_type = int_or_real(highest_prior(lhs.type, rhs.type))
            # if (int_or_real(lhs.type) != higher_data_type):
            #     tmp = ST.get_temp_var()
            #     tac.emit(tmp, lhs.place, '', int_or_real(lhs.type) +
            #              '_' + int_or_real(higher_data_type) + '_' + '=')
            #     tac.emit(self.place, tmp, rhs.place,
            #              higher_data_type+'_'+operator)
            # elif (int_or_real(rhs.type) != higher_data_type):
            #     tmp = ST.get_temp_var()
            #     tac.emit(tmp, rhs.place, '', int_or_real(rhs.type) +
            #              '_' + int_or_real(higher_data_type) + '_' + '=')
            #     tac.emit(self.place, lhs.place, tmp,
            #              higher_data_type + '_' + operator)
            # else:
            #     if lhs.type == 'char':
            #         tmp1 = ST.get_temp_var()
            #         tac.emit(tmp1, lhs.place, '', int_or_real('char') +
            #                  '_' + int_or_real('int') + '_' + '=')
            #         tmp2 = ST.get_temp_var()
            #         tac.emit(tmp2, rhs.place, '', int_or_real('char') +
            #                  '_' + int_or_real('int') + '_' + '=')
            #         tmp3 = ST.get_temp_var()
            #         tac.emit(tmp3, tmp1, tmp2, 'int_' + operator)
            #         tac.emit(self.place, tmp3, '', int_or_real('int') +
            #                  '_' + int_or_real('char') + '_' + '=')
            #     else:
            #         tac.emit(self.place, lhs.place, rhs.place,
            #                  int_or_real(lhs.type) + '_' + operator)


# BG start

class Conditional(Expression):

    def __init__(self, predicate, if_true, if_false):
        super(self.__class__, self).__init__()
        self._fields = ['predicate', 'if_true', 'if_false', 'type', 'place']
        parent_scope = ST.get_parent_scope()
        self.predicate = predicate
        self.if_true = if_true
        self.if_false = if_false
        self.place = None

        if predicate.type in ['int', 'float', 'bool', 'long', 'double'] and if_true.type == if_false.type:
            self.type = if_true.type
        elif if_true.type not in ['int', 'float', 'bool', 'long', 'double'] or if_false.type not in ['int', 'float', 'bool', 'long', 'double']:
            print("Type error in conditional expression.")


class ConditionalOr(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        self.type = 'bool'
        name = ST.get_temp_var()
        self.place = name
        # #tac.emit(name, lhs.place, rhs.place, operator+self.type)
        # if self.type in ['int', 'char', 'long']:
        #     tac.emit(name, lhs.place, rhs.place, operator+'int')
        # elif self.type in ['float', 'double']:
        #     tac.emit(name, lhs.place, rhs.place, operator+'float')
        # else:
        #     tac.emit(name, lhs.place, rhs.place, operator+self.type)

        higher_data_type = int_or_real(highest_prior(lhs.type, rhs.type))
        if (int_or_real(lhs.type) != higher_data_type):
            tmp = ST.get_temp_var()
            tac.emit(tmp, lhs.place, '', int_or_real(lhs.type) +
                     '_' + int_or_real(higher_data_type) + '_' + '=')
            tac.emit(self.place, tmp, rhs.place,
                     higher_data_type+'_'+operator)
        elif (int_or_real(rhs.type) != higher_data_type):
            tmp = ST.get_temp_var()
            tac.emit(tmp, rhs.place, '', int_or_real(rhs.type) +
                     '_' + int_or_real(higher_data_type) + '_' + '=')
            tac.emit(self.place, lhs.place, tmp,
                     higher_data_type + '_' + operator)
        else:
            if lhs.type == 'char':
                tmp1 = ST.get_temp_var()
                tac.emit(tmp1, lhs.place, '', int_or_real('char') +
                         '_' + int_or_real('int') + '_' + '=')
                tmp2 = ST.get_temp_var()
                tac.emit(tmp2, rhs.place, '', int_or_real('char') +
                         '_' + int_or_real('int') + '_' + '=')
                tmp3 = ST.get_temp_var()
                tac.emit(tmp3, tmp1, tmp2, 'int_' + operator)
                tac.emit(self.place, tmp3, '', int_or_real('int') +
                         '_' + int_or_real('char') + '_' + '=')
            else:
                tac.emit(self.place, lhs.place, rhs.place,
                         int_or_real(lhs.type) + '_' + operator)


class ConditionalAnd(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        self.type = 'bool'
        name = ST.get_temp_var()
        self.place = name
        #tac.emit(name, lhs.place, rhs.place, operator+self.type)
        # if self.type in ['int', 'char', 'long']:
        #     tac.emit(name, lhs.place, rhs.place, operator+'int')
        # elif self.type in ['float', 'double']:
        #     tac.emit(name, lhs.place, rhs.place, operator+'float')
        # else:
        #     tac.emit(name, lhs.place, rhs.place, operator+self.type)

        higher_data_type = int_or_real(highest_prior(lhs.type, rhs.type))
        if (int_or_real(lhs.type) != higher_data_type):
            tmp = ST.get_temp_var()
            tac.emit(tmp, lhs.place, '', int_or_real(lhs.type) +
                     '_' + int_or_real(higher_data_type) + '_' + '=')
            tac.emit(self.place, tmp, rhs.place,
                     higher_data_type+'_'+operator)
        elif (int_or_real(rhs.type) != higher_data_type):
            tmp = ST.get_temp_var()
            tac.emit(tmp, rhs.place, '', int_or_real(rhs.type) +
                     '_' + int_or_real(higher_data_type) + '_' + '=')
            tac.emit(self.place, lhs.place, tmp,
                     higher_data_type + '_' + operator)
        else:
            if lhs.type == 'char':
                tmp1 = ST.get_temp_var()
                tac.emit(tmp1, lhs.place, '', int_or_real('char') +
                         '_' + int_or_real('int') + '_' + '=')
                tmp2 = ST.get_temp_var()
                tac.emit(tmp2, rhs.place, '', int_or_real('char') +
                         '_' + int_or_real('int') + '_' + '=')
                tmp3 = ST.get_temp_var()
                tac.emit(tmp3, tmp1, tmp2, 'int_' + operator)
                tac.emit(self.place, tmp3, '', int_or_real('int') +
                         '_' + int_or_real('char') + '_' + '=')
            else:
                tac.emit(self.place, lhs.place, rhs.place,
                         int_or_real(lhs.type) + '_' + operator)


class Or(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        if lhs.type in ['int', 'char', 'long', 'bool'] and rhs.type in ['int', 'char', 'long', 'bool']:
            self.type = highest_prior(lhs.type, rhs.type)
            name = ST.get_temp_var()
            self.place = name
            # #tac.emit(name, lhs.place, rhs.place, operator+self.type)
            # if self.type in ['int', 'char', 'long']:
            #     tac.emit(name, lhs.place, rhs.place, operator+'int')
            # elif self.type in ['float', 'double']:
            #     tac.emit(name, lhs.place, rhs.place, operator+'float')
            # else:
            #     tac.emit(name, lhs.place, rhs.place, operator+self.type)
            higher_data_type = int_or_real(highest_prior(lhs.type, rhs.type))
            if (int_or_real(lhs.type) != higher_data_type):
                tmp = ST.get_temp_var()
                tac.emit(tmp, lhs.place, '', int_or_real(lhs.type) +
                         '_' + int_or_real(higher_data_type) + '_' + '=')
                tac.emit(self.place, tmp, rhs.place,
                         higher_data_type+'_'+operator)
            elif (int_or_real(rhs.type) != higher_data_type):
                tmp = ST.get_temp_var()
                tac.emit(tmp, rhs.place, '', int_or_real(rhs.type) +
                         '_' + int_or_real(higher_data_type) + '_' + '=')
                tac.emit(self.place, lhs.place, tmp,
                         higher_data_type + '_' + operator)
            else:
                if lhs.type == 'char':
                    tmp1 = ST.get_temp_var()
                    tac.emit(tmp1, lhs.place, '', int_or_real('char') +
                             '_' + int_or_real('int') + '_' + '=')
                    tmp2 = ST.get_temp_var()
                    tac.emit(tmp2, rhs.place, '', int_or_real('char') +
                             '_' + int_or_real('int') + '_' + '=')
                    tmp3 = ST.get_temp_var()
                    tac.emit(tmp3, tmp1, tmp2, 'int_' + operator)
                    tac.emit(self.place, tmp3, '', int_or_real('int') +
                             '_' + int_or_real('char') + '_' + '=')
                else:
                    tac.emit(self.place, lhs.place, rhs.place,
                             int_or_real(lhs.type) + '_' + operator)

        else:
            print("Error in Or operator operand types.")


class Xor(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        if lhs.type in ['int', 'char', 'long', 'bool'] and rhs.type in ['int', 'char', 'long', 'bool']:
            self.type = highest_prior(lhs.type, rhs.type)
            name = ST.get_temp_var()
            self.place = name
            #tac.emit(name, lhs.place, rhs.place, operator+self.type)
            # if self.type in ['int', 'char', 'long']:
            #     tac.emit(name, lhs.place, rhs.place, operator+'int')
            # elif self.type in ['float', 'double']:
            #     tac.emit(name, lhs.place, rhs.place, operator+'float')
            # else:
            #     tac.emit(name, lhs.place, rhs.place, operator+self.type)

            higher_data_type = int_or_real(highest_prior(lhs.type, rhs.type))
            if (int_or_real(lhs.type) != higher_data_type):
                tmp = ST.get_temp_var()
                tac.emit(tmp, lhs.place, '', int_or_real(lhs.type) +
                         '_' + int_or_real(higher_data_type) + '_' + '=')
                tac.emit(self.place, tmp, rhs.place,
                         higher_data_type+'_'+operator)
            elif (int_or_real(rhs.type) != higher_data_type):
                tmp = ST.get_temp_var()
                tac.emit(tmp, rhs.place, '', int_or_real(rhs.type) +
                         '_' + int_or_real(higher_data_type) + '_' + '=')
                tac.emit(self.place, lhs.place, tmp,
                         higher_data_type + '_' + operator)
            else:
                if lhs.type == 'char':
                    tmp1 = ST.get_temp_var()
                    tac.emit(tmp1, lhs.place, '', int_or_real('char') +
                             '_' + int_or_real('int') + '_' + '=')
                    tmp2 = ST.get_temp_var()
                    tac.emit(tmp2, rhs.place, '', int_or_real('char') +
                             '_' + int_or_real('int') + '_' + '=')
                    tmp3 = ST.get_temp_var()
                    tac.emit(tmp3, tmp1, tmp2, 'int_' + operator)
                    tac.emit(self.place, tmp3, '', int_or_real('int') +
                             '_' + int_or_real('char') + '_' + '=')
                else:
                    tac.emit(self.place, lhs.place, rhs.place,
                             int_or_real(lhs.type) + '_' + operator)

        else:
            print("Error in Xor operator operand types.")


class And(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        if lhs.type in ['int', 'char', 'long', 'bool'] and rhs.type in ['int', 'char', 'long', 'bool']:
            self.type = highest_prior(lhs.type, rhs.type)
            name = ST.get_temp_var()
            self.place = name
            #tac.emit(name, lhs.place, rhs.place, operator+self.type)
            # if self.type in ['int', 'char', 'long']:
            #     tac.emit(name, lhs.place, rhs.place, operator+'int')
            # elif self.type in ['float', 'double']:
            #     tac.emit(name, lhs.place, rhs.place, operator+'float')
            # else:
            #     tac.emit(name, lhs.place, rhs.place, operator+self.type)

            higher_data_type = int_or_real(highest_prior(lhs.type, rhs.type))
            if (int_or_real(lhs.type) != higher_data_type):
                tmp = ST.get_temp_var()
                tac.emit(tmp, lhs.place, '', int_or_real(lhs.type) +
                         '_' + int_or_real(higher_data_type) + '_' + '=')
                tac.emit(self.place, tmp, rhs.place,
                         higher_data_type+'_'+operator)
            elif (int_or_real(rhs.type) != higher_data_type):
                tmp = ST.get_temp_var()
                tac.emit(tmp, rhs.place, '', int_or_real(rhs.type) +
                         '_' + int_or_real(higher_data_type) + '_' + '=')
                tac.emit(self.place, lhs.place, tmp,
                         higher_data_type + '_' + operator)
            else:
                if lhs.type == 'char':
                    tmp1 = ST.get_temp_var()
                    tac.emit(tmp1, lhs.place, '', int_or_real('char') +
                             '_' + int_or_real('int') + '_' + '=')
                    tmp2 = ST.get_temp_var()
                    tac.emit(tmp2, rhs.place, '', int_or_real('char') +
                             '_' + int_or_real('int') + '_' + '=')
                    tmp3 = ST.get_temp_var()
                    tac.emit(tmp3, tmp1, tmp2, 'int_' + operator)
                    tac.emit(self.place, tmp3, '', int_or_real('int') +
                             '_' + int_or_real('char') + '_' + '=')
                else:
                    tac.emit(self.place, lhs.place, rhs.place,
                             int_or_real(lhs.type) + '_' + operator)

        else:
            print("Error in And operator operand types.")


class Equality(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        if lhs.type in ['int', 'char', 'long', 'bool', 'float', 'double'] and rhs.type in ['int', 'char', 'long', 'bool', 'float', 'double']:
            name = ST.get_temp_var()
            self.place = name
            #tac.emit(name, lhs.place, rhs.place, operator+self.type)
            # if self.type in ['int', 'char', 'long']:
            #     tac.emit(name, lhs.place, rhs.place, operator+'int')
            # elif self.type in ['float', 'double']:
            #     tac.emit(name, lhs.place, rhs.place, operator+'float')
            # else:
            #     tac.emit(name, lhs.place, rhs.place, operator+self.type)

            higher_data_type = int_or_real(highest_prior(lhs.type, rhs.type))
            if (int_or_real(lhs.type) != higher_data_type):
                tmp = ST.get_temp_var()
                tac.emit(tmp, lhs.place, '', int_or_real(lhs.type) +
                         '_' + int_or_real(higher_data_type) + '_' + '=')
                tac.emit(self.place, tmp, rhs.place,
                         higher_data_type+'_'+operator)
            elif (int_or_real(rhs.type) != higher_data_type):
                tmp = ST.get_temp_var()
                tac.emit(tmp, rhs.place, '', int_or_real(rhs.type) +
                         '_' + int_or_real(higher_data_type) + '_' + '=')
                tac.emit(self.place, lhs.place, tmp,
                         higher_data_type + '_' + operator)
            else:
                if lhs.type == 'char':
                    tmp1 = ST.get_temp_var()
                    tac.emit(tmp1, lhs.place, '', int_or_real('char') +
                             '_' + int_or_real('int') + '_' + '=')
                    tmp2 = ST.get_temp_var()
                    tac.emit(tmp2, rhs.place, '', int_or_real('char') +
                             '_' + int_or_real('int') + '_' + '=')
                    tmp3 = ST.get_temp_var()
                    tac.emit(tmp3, tmp1, tmp2, 'int_' + operator)
                    tac.emit(self.place, tmp3, '', int_or_real('int') +
                             '_' + int_or_real('char') + '_' + '=')
                else:
                    tac.emit(self.place, lhs.place, rhs.place,
                             int_or_real(lhs.type) + '_' + operator)

            self.type = 'bool'
            self.falselist = [len(tac.code)]
            if self.type in ['int', 'long']:
                tac.emit("ifgoto", self.place, 'eq0', '')
            elif self.type in ['float', 'double']:
                tac.emit("ifgoto", self.place, 'eq0.0', '')
            else:
                tac.emit("ifgoto", self.place, 'eq0c', '')
            self.truelist = [len(tac.code)]
           # tac.emit("goto", '', '', '')
        else:
            print("Error in == operator operand types.")


class Relational(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        if lhs.type in ['int', 'char', 'long', 'bool', 'float', 'double'] and rhs.type in ['int', 'char', 'long', 'bool', 'float', 'double']:
            name = ST.get_temp_var()
            self.place = name
            #tac.emit(name, lhs.place, rhs.place, operator+self.type)
            # if self.type in ['int', 'char', 'long']:
            #     tac.emit(name, lhs.place, rhs.place, operator+'int')
            # elif self.type in ['float', 'double']:
            #     tac.emit(name, lhs.place, rhs.place, operator+'float')
            # else:
            #     tac.emit(name, lhs.place, rhs.place, operator+self.type)

            higher_data_type = int_or_real(highest_prior(lhs.type, rhs.type))
            if (int_or_real(lhs.type) != higher_data_type):
                tmp = ST.get_temp_var()
                tac.emit(tmp, lhs.place, '', int_or_real(lhs.type) +
                         '_' + int_or_real(higher_data_type) + '_' + '=')
                tac.emit(self.place, tmp, rhs.place,
                         higher_data_type+'_'+operator)
            elif (int_or_real(rhs.type) != higher_data_type):
                tmp = ST.get_temp_var()
                tac.emit(tmp, rhs.place, '', int_or_real(rhs.type) +
                         '_' + int_or_real(higher_data_type) + '_' + '=')
                tac.emit(self.place, lhs.place, tmp,
                         higher_data_type + '_' + operator)
            else:
                if lhs.type == 'char':
                    tmp1 = ST.get_temp_var()
                    tac.emit(tmp1, lhs.place, '', int_or_real('char') +
                             '_' + int_or_real('int') + '_' + '=')
                    tmp2 = ST.get_temp_var()
                    tac.emit(tmp2, rhs.place, '', int_or_real('char') +
                             '_' + int_or_real('int') + '_' + '=')
                    tmp3 = ST.get_temp_var()
                    tac.emit(tmp3, tmp1, tmp2, 'int_' + operator)
                    tac.emit(self.place, tmp3, '', int_or_real('int') +
                             '_' + int_or_real('char') + '_' + '=')
                else:
                    tac.emit(self.place, lhs.place, rhs.place,
                             int_or_real(lhs.type) + '_' + operator)

            self.type = 'bool'
            self.falselist = [len(tac.code)]
#            tac.emit("ifgoto", self.place, 'eq0', '')
            if self.type in ['int', 'long']:
                tac.emit("ifgoto", self.place, 'eq0', '')
            elif self.type in ['float', 'double']:
                tac.emit("ifgoto", self.place, 'eq0.0', '')
            else:
                tac.emit("ifgoto", self.place, 'eq0c', '')
            self.truelist = [len(tac.code)]
          #  tac.emit("goto", '', '', '')
        else:
            print("Error in relational operator operand types.")


class Shift(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        if lhs.type in ['int', 'char', 'long'] and rhs.type in ['int', 'char', 'long']:
            self.type = highest_prior(lhs.type, rhs.type)
            name = ST.get_temp_var()
            self.place = name
            #tac.emit(name, lhs.place, rhs.place, operator+self.type)
            # if self.type in ['int', 'char', 'long']:
            #     tac.emit(name, lhs.place, rhs.place, operator+'int')
            # elif self.type in ['float', 'double']:
            #     tac.emit(name, lhs.place, rhs.place, operator+'float')
            # else:
            #     tac.emit(name, lhs.place, rhs.place, operator+self.type)

            higher_data_type = int_or_real(highest_prior(lhs.type, rhs.type))
            if (int_or_real(lhs.type) != higher_data_type):
                tmp = ST.get_temp_var()
                tac.emit(tmp, lhs.place, '', int_or_real(lhs.type) +
                         '_' + int_or_real(higher_data_type) + '_' + '=')
                tac.emit(self.place, tmp, rhs.place,
                         higher_data_type+'_'+operator)
            elif (int_or_real(rhs.type) != higher_data_type):
                tmp = ST.get_temp_var()
                tac.emit(tmp, rhs.place, '', int_or_real(rhs.type) +
                         '_' + int_or_real(higher_data_type) + '_' + '=')
                tac.emit(self.place, lhs.place, tmp,
                         higher_data_type + '_' + operator)
            else:
                if lhs.type == 'char':
                    tmp1 = ST.get_temp_var()
                    tac.emit(tmp1, lhs.place, '', int_or_real('char') +
                             '_' + int_or_real('int') + '_' + '=')
                    tmp2 = ST.get_temp_var()
                    tac.emit(tmp2, rhs.place, '', int_or_real('char') +
                             '_' + int_or_real('int') + '_' + '=')
                    tmp3 = ST.get_temp_var()
                    tac.emit(tmp3, tmp1, tmp2, 'int_' + operator)
                    tac.emit(self.place, tmp3, '', int_or_real('int') +
                             '_' + int_or_real('char') + '_' + '=')
                else:
                    tac.emit(self.place, lhs.place, rhs.place,
                             int_or_real(lhs.type) + '_' + operator)
        else:
            print("Error in Shift operator operand types.")


class Additive(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        if lhs.type in ['int', 'char', 'long', 'bool', 'float', 'double'] and rhs.type in ['int', 'char', 'long', 'bool', 'float', 'double']:
            self.type = highest_prior(lhs.type, rhs.type)
            name = ST.get_temp_var()
            self.place = name
            #tac.emit(name, lhs.place, rhs.place, operator+self.type)
            # if self.type in ['int', 'char', 'long']:
            #     tac.emit(name, lhs.place, rhs.place, operator+'int')
            # elif self.type in ['float', 'double']:
            #     tac.emit(name, lhs.place, rhs.place, operator+'float')
            # else:
            #     tac.emit(name, lhs.place, rhs.place, operator+self.type)
            ###########
            higher_data_type = int_or_real(highest_prior(lhs.type, rhs.type))
            if (int_or_real(lhs.type) != higher_data_type):
                tmp = ST.get_temp_var()
                tac.emit(tmp, lhs.place, '', int_or_real(lhs.type) +
                         '_' + int_or_real(higher_data_type) + '_' + '=')
                tac.emit(self.place, tmp, rhs.place,
                         higher_data_type+'_'+operator)
            elif (int_or_real(rhs.type) != higher_data_type):
                tmp = ST.get_temp_var()
                tac.emit(tmp, rhs.place, '', int_or_real(rhs.type) +
                         '_' + int_or_real(higher_data_type) + '_' + '=')
                tac.emit(self.place, lhs.place, tmp,
                         higher_data_type + '_' + operator)
            else:
                if lhs.type == 'char':
                    tmp1 = ST.get_temp_var()
                    tac.emit(tmp1, lhs.place, '', int_or_real('char') +
                             '_' + int_or_real('int') + '_' + '=')
                    tmp2 = ST.get_temp_var()
                    tac.emit(tmp2, rhs.place, '', int_or_real('char') +
                             '_' + int_or_real('int') + '_' + '=')
                    tmp3 = ST.get_temp_var()
                    tac.emit(tmp3, tmp1, tmp2, 'int_' + operator)
                    tac.emit(self.place, tmp3, '', int_or_real('int') +
                             '_' + int_or_real('char') + '_' + '=')
                else:
                    tac.emit(self.place, lhs.place, rhs.place,
                             int_or_real(lhs.type) + '_' + operator)
                #######################
        else:
            print("Error in additive operator operand types.")


class Multiplicative(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        if lhs.type in ['int', 'char', 'long', 'bool', 'float', 'double'] and rhs.type in ['int', 'char', 'long', 'bool', 'float', 'double']:
            self.type = highest_prior(lhs.type, rhs.type)
            name = ST.get_temp_var()
            self.place = name
            # #tac.emit(name, lhs.place, rhs.place, operator)
            # if self.type in ['int', 'char', 'long']:
            #     tac.emit(name, lhs.place, rhs.place, operator+'int')
            # elif self.type in ['float', 'double']:
            #     tac.emit(name, lhs.place, rhs.place, operator+'float')
            # else:
            #     tac.emit(name, lhs.place, rhs.place, operator+self.type)
            ###########
            higher_data_type = int_or_real(highest_prior(lhs.type, rhs.type))
            if (int_or_real(lhs.type) != higher_data_type):
                tmp = ST.get_temp_var()
                tac.emit(tmp, lhs.place, '', int_or_real(lhs.type) +
                         '_' + int_or_real(higher_data_type) + '_' + '=')
                tac.emit(self.place, tmp, rhs.place,
                         higher_data_type+'_'+operator)
            elif (int_or_real(rhs.type) != higher_data_type):
                tmp = ST.get_temp_var()
                tac.emit(tmp, rhs.place, '', int_or_real(rhs.type) +
                         '_' + int_or_real(higher_data_type) + '_' + '=')
                tac.emit(self.place, lhs.place, tmp,
                         higher_data_type + '_' + operator)
            else:
                if lhs.type == 'char':
                    tmp1 = ST.get_temp_var()
                    tac.emit(tmp1, lhs.place, '', int_or_real('char') +
                             '_' + int_or_real('int') + '_' + '=')
                    tmp2 = ST.get_temp_var()
                    tac.emit(tmp2, rhs.place, '', int_or_real('char') +
                             '_' + int_or_real('int') + '_' + '=')
                    tmp3 = ST.get_temp_var()
                    tac.emit(tmp3, tmp1, tmp2, 'int_' + operator)
                    tac.emit(self.place, tmp3, '', int_or_real('int') +
                             '_' + int_or_real('char') + '_' + '=')
                else:
                    tac.emit(self.place, lhs.place, rhs.place,
                             int_or_real(lhs.type) + '_' + operator)
                #######################
        else:
            print("Error in multiplicative operator operand types.")


class Unary(Expression):

    def __init__(self, sign, expression):
        super(Unary, self).__init__()
        self._fields = ['sign', 'expression', 'type', 'place']
        self.sign = sign
        self.expression = expression
        self.type = expression.type
        self.place = expression.place

        temp = ST.get_temp_var()
        if "++" in sign or "--" in sign:
            if "++" == sign[1:3] or "--" == sign[1:3]:
                temp1 = ST.get_temp_var()
                #tac.emit(temp1, expression.place, ' ', '='+self.type)
                if self.type in ['int', 'char', 'long']:
                    tac.emit(temp1, expression.place, ' ', '='+'int')
                elif self.type in ['float', 'double']:
                    tac.emit(temp1, expression.place, ' ', '='+'float')
                else:
                    tac.emit(temp1, expression.place, ' ', '='+self.type)

                self.place = temp1
            if "++" in sign:
                #tac.emit(temp, expression.place, '1', '+'+self.type)
                #tac.emit(expression.place, temp, ' ', '='+self.type)
                if self.type in ['int', 'char', 'long']:
                    tac.emit(temp, expression.place, '1', '+'+'int')
                    tac.emit(expression.place, temp, ' ', '='+'int')
                elif self.type in ['float', 'double']:
                    tac.emit(temp, expression.place, '1', '+'+'float')
                    tac.emit(expression.place, temp, ' ', '='+'float')
                else:
                    tac.emit(temp, expression.place, '1', '+'+self.type)
                    tac.emit(expression.place, temp, ' ', '='+self.type)

            elif "--" in sign:
                #tac.emit(temp, expression.place, '1', '-'+self.type)
                #tac.emit(expression.place, temp, ' ', '='+self.type)
                if self.type in ['int', 'char', 'long']:
                    tac.emit(temp, expression.place, '1', '-'+'int')
                    tac.emit(expression.place, temp, ' ', '='+'int')
                elif self.type in ['float', 'double']:
                    tac.emit(temp, expression.place, '1', '-'+'float')
                    tac.emit(expression.place, temp, ' ', '='+'float')
                else:
                    tac.emit(temp, expression.place, '1', '-'+self.type)
                    tac.emit(expression.place, temp, ' ', '='+self.type)
        elif "-" in sign:
            if isinstance(self.expression, Literal):
                self.place = '-' + self.expression.place
            else:
                #tac.emit('neg', expression.place, ' ', self.type)
                if self.type in ['int', 'char', 'long']:
                    tac.emit('neg', expression.place, ' ', 'int')
                elif self.type in ['float', 'double']:
                    tac.emit('neg', expression.place, ' ', 'float')
                else:
                    tac.emit('neg', expression.place, ' ', self.type)

# TODO shift operations


class Cast(Expression):

    def __init__(self, target, expression):
        super(Cast, self).__init__()
        self._fields = ['target', 'expression', 'type', 'place']
        self.target = target
        self.expression = expression
        self.type = target.name
        self.place = expression.place


class Statement(BaseClass):
    pass


class Empty(Statement):
    pass


class Block(Statement):

    def __init__(self, statements=None):
        super(Statement, self).__init__()
        self._fields = ['statements']
        if statements is None:
            statements = []
        self.statements = statements

    def __iter__(self):
        for s in self.statements:
            yield s


class VariableDeclaration(Statement, FieldDeclaration):
    pass


class ArrayInitializer(BaseClass):
    def __init__(self, elements=None):
        super(ArrayInitializer, self).__init__()
        self._fields = ['elements']
        if elements is None:
            elements = []
        self.elements = elements


class MethodInvocation(Expression):
    def __init__(self, name, arguments=None, type_arguments=None, target=None):
        super(MethodInvocation, self).__init__()
        self._fields = ['name', 'arguments',
                        'type_arguments', 'target', 'type', 'place']
        func_name = None
        a = name
        if type(name) != str:
            a = name.value
        temp = ST.curr_scope
        temp_table = ST.scope_and_table_map[ST.curr_scope]
        f_type = None
        varx = ""
        if target != None:
            if target == 'this':
                new_var = ST.get_temp_var()
                tac.emit(new_var, 'EXTRACT_THIS', '', '=')
                t = ST.scope_and_table_map[ST.curr_scope]

                while t.scope_type != 'class':
                    t = t.parent_table
                ST.curr_scope = t.scope
            elif hasattr(target, 'type'):
                ST.curr_scope = target.type
            ST.curr_sym_table = ST.scope_and_table_map[ST.curr_scope]
        # if '.' in a:
        if True:
            a = a.split(".")
            varx = a[0]
            for var in a:
                # print("here",var)
                # print(get_func_name(var, arguments))

                if ST.lookup(var) == None and ST.lookup(get_func_name(var, arguments), is_func=True) == None:
                    print("Variable/Function", var,
                          f"not declared in current scope {ST.curr_scope} (1)")
                    break
                elif ST.lookup(var) != None and ST.lookup(var)['type'] not in primitives:
                    if 'private' in ST.lookup(var)['modifiers'] and not ST.check_parent_child_relationship(ST.lookup(var)['scope'], temp):
                        print(
                            f"Tried to access a 'private' variable '{var}' from outside 1")
                        break
                    k = ST.lookup(var)['type']
                    ST.curr_scope = k
                    ST.curr_sym_table = ST.scope_and_table_map[ST.curr_scope]
                    f_type = k
                elif ST.lookup(get_func_name(var, arguments), is_func=True) != None:
                    if 'private' in ST.lookup(get_func_name(var, arguments), is_func=True)['modifiers'] and not ST.check_parent_child_relationship(ST.lookup(get_func_name(var, arguments), is_func=True)['scope'], temp):
                        # print(get_func_name(var, arguments))
                        print(
                            f"Tried to access a 'private' function '{var}' from outside")
                        break
                    func_name = get_func_name(var, arguments)
                    t = ST.curr_scope
                    f_type = ST.lookup(get_func_name(var, arguments), is_func=True)[
                        'return_type']
                    ST.curr_scope = ST.lookup(get_func_name(
                        var, arguments), is_func=True)['name']
                    ST.curr_sym_table = ST.scope_and_table_map[ST.curr_scope]
                elif ST.lookup(var) != None and ST.lookup(var)['type'] in primitives:
                    if 'private' in ST.lookup(var)['modifiers'] and not ST.check_parent_child_relationship(ST.lookup(var)['scope'], temp):
                        print(
                            f"Tried to access a 'private' variable '{var}' from outside 2")
                        break
                    f_type = ST.lookup(var)['type']

            self.type = f_type

            if hasattr(name, 'value'):
                name.value = var
            else:
                name = Name(var)
        # else:
        #     if hasattr(target, 'type'):
        #         ST.curr_scope=target.type
        #         ST.curr_sym_table=ST.scope_and_table_map[ST.curr_scope]
        #     else:
        #         ST.curr_scope=temp
        #         ST.curr_sym_table=temp_table

        if arguments is None:
            arguments = []
        self.name = name
        self.arguments = arguments
        self.target = target
        self.type = None
        self.type_arguments = type_arguments
        try:
            if ST.lookup(ST.curr_scope, is_func=True) is None:
                print("Not a function")
            else:
                n_params = ST.lookup(ST.curr_scope, is_func=True)['n_params']
                self.type = ST.lookup(ST.curr_scope, is_func=True)[
                    'return_type']
                params = ST.lookup(ST.curr_scope, is_func=True)['params']
                if n_params != len(arguments):
                    print('Incorrect number of Arguements')
                else:
                    for i in range(len(arguments)):
                        if arguments[i].type != params[i]['type']:
                            print('Type of method arguement not correct')
                            print(arguments[i].type, params[i]['type'])
        except:
            pass
        temp2 = ST.curr_scope
        temp_table2 = ST.curr_sym_table
        ST.curr_scope = temp
        ST.curr_sym_table = temp_table

        for x in reversed(self.arguments):
            if isinstance(x, Literal):
                tac.emit('push', x.value, '', '')

            elif isinstance(x, Name):
                tac.emit('push', x.value+'$' +
                         ST.lookup(x.value)['scope'], '', '')
            elif hasattr(x, 'place'):
                tac.emit('push', x.place, '', '')

        ST.curr_scope = temp2
        ST.curr_sym_table = temp_table2
        # tac.emit('push',varx,'','')
        ST.curr_scope = ST.get_parent_scope()
        ST.curr_sym_table = ST.curr_sym_table.parent_table
        old_var = ST.get_last_label()
        new_var = ST.get_temp_var()
        tac.emit(new_var, old_var, '', '=')
        # tac.emit(new_var, 'OFFSET OF '+ get_func_name(name.value, arguments), '', '-=')
        tac.emit('push', new_var, '', '')
        ST.curr_scope = ST.get_parent_scope()
        ST.curr_sym_table = ST.curr_sym_table.parent_table
        tac.emit('call', get_func_name(name.value, arguments),str(len(arguments)), '')
        new_var = ST.get_temp_var()
        for i in range(len(arguments)+1):
            tac.emit('pop', new_var, '', '')

        ST.curr_scope = temp
        ST.curr_sym_table = temp_table
        temp = ST.get_temp_var()
        # if func_name != None and ST.lookup(func_name ,is_func=True) != None and ST.lookup(func_name ,is_func=True)['return_type'] != 'void':
        #     tac.emit('pop',temp,'','')
        self.place = temp


class IfThenElse(Statement, ScopeField):

    def __init__(self, predicate, if_true=None, if_false=None):
        super(IfThenElse, self).__init__()
        self._fields = ['predicate', 'if_true', 'if_false']
        self.predicate = predicate
        self.if_true = if_true
        self.if_false = if_false


class While(Statement, ScopeField):

    def __init__(self, predicate, body=None):
        super(While, self).__init__()
        self._fields = ['predicate', 'body']
        self.predicate = predicate
        self.body = body


class For(Statement, ScopeField):

    def __init__(self, init, predicate, update, body):
        super(For, self).__init__()
        self._fields = ['init', 'predicate', 'update', 'body']
        self.init = init
        self.predicate = predicate
        self.update = update
        self.body = body


class Switch(Statement):

    def __init__(self, expression, switch_cases):
        super(Switch, self).__init__()
        self._fields = ['expression', 'switch_cases']
        self.expression = expression
        self.switch_cases = switch_cases

        if expression.type not in ['int', 'long', 'bool', 'char']:
            print('Error in switch expression type')


class SwitchCase(BaseClass):

    def __init__(self, cases, body=None):
        super(SwitchCase, self).__init__()
        self._fields = ['cases', 'body']
        if body is None:
            body = []
        self.cases = cases
        self.body = body


class DoWhile(Statement, ScopeField):

    def __init__(self, predicate, body=None):
        super(DoWhile, self).__init__()
        self._fields = ['predicate', 'body']
        self.predicate = predicate
        self.body = body


class Continue(Statement):

    def __init__(self, label=None):
        super(Continue, self).__init__()
        self._fields = ['label']
        self.label = label


class Break(Statement):

    def __init__(self, label=None):
        super(Break, self).__init__()
        self._fields = ['label']
        self.label = label


class Return(Statement):

    def __init__(self, result=None):
        super(Return, self).__init__()
        self._fields = ['result', 'type']
        self.result = result
        self.type = 'void'
        if result:
            self.type = result.type
        res = ST.get_curr_func()
        if not res:
            print("Not in a function")
        elif res['return_type'] == self.type or (res['return_type'] in primitives and self.type in primitives):
            pass
        else:
            print("Return type mismatch")

        if result:
            tac.emit('ret', result.place, '', '')
        else:
            tac.emit('ret', '', '', '')


class ConstructorInvocation(Statement):

    def __init__(self, name, target=None, arguments=None):
        super(ConstructorInvocation, self).__init__()
        self._fields = ['name', 'target', 'arguments']
        if arguments is None:
            arguments = []
        self.name = name
        self.target = target
        self.arguments = arguments


class InstanceCreation(Expression):

    def __init__(self, type, arguments=None, body=None):
        super(InstanceCreation, self).__init__()
        self._fields = ['type', 'arguments', 'body', 'place']
        if arguments is None:
            arguments = []
        if body is None:
            body = []
        self.type = type
        self.arguments = arguments
        self.body = body
        self.place = ST.get_temp_var()
        tac.emit(self.place, type, "", 'declare')
        if type in primitives: return
        temp_scope=ST.curr_scope
        temp_table=ST.curr_sym_table
        ST.curr_scope=type
        ST.curr_sym_table=ST.scope_and_table_map[type]
        if get_func_name(type, arguments) not in ST.curr_sym_table.functions.keys(): print(f"Constructor for {type} not declared")
        # print(get_func_name(type, arguments))
        for x in reversed(arguments):
            if isinstance(x, Literal): tac.emit('push',x.value,'','')
            elif isinstance(x, Name):
                tac.emit('push',x.value+'$'+ST.lookup(x.value)['scope'],'','')
            elif hasattr(x, 'place'):
                tac.emit('push',x.place,'','')
        tac.emit('push', self.place, '', '')
        tac.emit('call', get_func_name(type, arguments), '', '')
        new_var=ST.get_temp_var()
        for i in range(len(arguments)+1):
            tac.emit('pop', new_var, '', '')
        ST.curr_scope=temp_scope
        ST.curr_sym_table=temp_table



class FieldAccess(Expression):

    def __init__(self, name, target):
        super(FieldAccess, self).__init__()
        self._fields = ['name', 'target', 'type']
        self.name = name
        self.target = target
        if target == None:
            target = ''
        self.type = None
        self.place = name.place

        if target == 'this':
            # new_var=ST.get_temp_var()
            # tac.emit(new_var, 'EXTRACT_THIS', '', '=')

            self.type = name.type
            # self.place = name.value+'$'+ST.get_parent_class()


class ArrayAccess(Expression):

    def __init__(self, index, target):
        super(ArrayAccess, self).__init__()
        self._fields = ['index', 'target', 'type', 'depth',
                        'dimension', 'place', 'pass_dimension', 'len']
        self.index = index
        self.target = target
        self.type = target.type
        width=8
        if self.type in primitives: width=widths[self.type]
        if index.type not in ['int', 'long']:
            print('Array index not of type int')

        # while ST.lookup(target) is not None:
        #   target=target.target

        if target.__class__ == ArrayAccess:
            self.depth = target.depth + 1
            self.dimension = target.dimension
        else:
            self.depth = 1
            value = ST.lookup(target.value)
            self.dimension = value['dims']
        if self.depth > self.dimension:
            print("More than allowed dimension(s) accessed")
        # if self.depth < self.dimension:
        #     print("Less than allowed dimension(s) accessed")

        if self.depth == 1:
            self.array = target.place
            value = ST.lookup(target.value)
            dimensions = value['arr_size']
            self.pass_dimension = dimensions

            length = 1
            for x in dimensions[self.depth:]:
                length *= int(x)
            temp = ST.get_temp_var()
            tac.emit(temp, index.place, width*length, '*')

            self.len = temp
            self.place = self.array + '['+temp+']'

        else:
            dimensions = target.pass_dimension
            length = 1
            for x in dimensions[self.depth:]:
                length *= int(x)
            temp = ST.get_temp_var()
            tac.emit(temp, index.place, width*length, '*')
            temp1 = ST.get_temp_var()
            tac.emit(temp1, temp, target.len, '+')
            self.place = temp1
            self.array = target.array
            if self.depth == len(dimensions):
                self.place = self.array + '['+temp1+']'
            self.pass_dimension = dimensions
            self.len = temp1


class ArrayCreation(Expression):

    def __init__(self, type, dimensions=None, initializer=None):
        super(ArrayCreation, self).__init__()
        self._fields = ['type', 'dimensions', 'initializer']
        if dimensions is None:
            dimensions = []
        self.type = type
        self.dimensions = dimensions
        self.initializer = initializer


class Literal(BaseClass):

    def __init__(self, value):
        super(Literal, self).__init__()
        self._fields = ['value', 'type', 'place']
        self.value = value
        self.place = value
        if value[0] == "'":
            self.type = 'char'
        elif value[0] == '"':
            self.type = 'str'
        elif self.value.find('.') == 1:
            self.type = 'double'
        elif value == "NULL":
            self.type = 'null'
        elif value == 'true' or value == 'false':
            self.type = 'bool'
        else:
            self.type = 'int'


class Name(BaseClass):

    def __init__(self, value, type=None):
        super(Name, self).__init__()
        self._fields = ['value', 'type', 'place']
        self.value = value
        self.type = type
        var = None
        var2 = value
        if ST.lookup(value) != None:
            # print(ST.lookup(value))
            var = value+'$'+ST.lookup(value)['scope']
        elif ST.lookup(value, is_func=True) != None:
            var = get_func_name(value)+'$'+ST.lookup(value,
                                                     is_func=True)['scope']
            # TODO
            # var2=get_func_name(value)
        else:
            # print(value)
            # TODO
            # print("Not in Scope")
            return
        self.place = var
        if type:
            return
        # if ST.lookup(value) == None and ST.lookup(value+'_'+ST.curr_scope,is_func=True) == None:
           # print("Variable/Function",value, f"not declared in current scope {ST.curr_scope} (2)")
        if ST.lookup(value) != None:
            self.type = ST.lookup(value)['type']
        else:
            self.type = "$func"

    def append_name(self, name):
        try:
            self.value = self.value + '.' + name.value
        except:
            self.value = self.value + '.' + name

        a = self.value
        a = a.split(".")
        temp = ST.curr_scope
        temp_table = ST.scope_and_table_map[ST.curr_scope]
        f_type = None
        for var in a:
            if var=='':continue
            if f_type in primitives:
                print("primitive type")
            if ST.lookup(var) != None and ST.lookup(var)['type'] not in primitives:
                if 'private' in ST.lookup(var)['modifiers'] and not ST.check_parent_child_relationship(ST.lookup(var)['scope'], temp):
                    print(
                        f"Tried to access a 'private' variable '{var}' from outside 3")
                    break
                k = ST.lookup(var)['type']
                ST.curr_scope = k
                ST.curr_sym_table = ST.scope_and_table_map[ST.curr_scope]
                f_type = k
            elif ST.lookup(var) != None and ST.lookup(var)['type'] in primitives:
                if 'private' in ST.lookup(var)['modifiers'] and not ST.check_parent_child_relationship(ST.lookup(var)['scope'], temp):
                    print(
                        f"Tried to access a 'private' variable '{var}' from outside 4")
                    break
                f_type = ST.lookup(var)['type']
            elif ST.check_func_prefix(var) == True:
                f_type = '$func'
            else:
                print(f"{var} not declared in current scope")

        # print(self.value, self.type, self.place, name)
        # Say, temp var stores the address of the variable
        # for field access, first of all copy self.place to a new variable
        # increment the new variable with offset
        # dereference the variable and store it in new variable
        new_var = ST.get_temp_var()
        # print(name, self.type)
        tac.emit(new_var, '', self.place, '=')
        offset = ST.get_offset(self.type, name)

        if offset != None:
            tac.emit(new_var, '', str(offset), '+=')
            if f_type not in primitives: tac.emit(new_var, '', new_var, 'DEREFERENCE')
        else:
            pass

        # emit self.place = self.type.offset
        # tac.emit()
        self.place = new_var
        ST.curr_scope = temp
        ST.curr_sym_table = temp_table
        self.type = f_type
        # print(name)


class ExpressionStatement(Statement):
    def __init__(self, expression):
        super(ExpressionStatement, self).__init__()
        self._fields = ['expression']
        self.expression = expression
