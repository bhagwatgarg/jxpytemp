widths = {'int':4, 'float':8, 'short':4, 'long':8, 'double':8, 'char':1}
count = -1
from new_sym_table import ScopeTable
from tac import TAC

ST = ScopeTable()
# all_types=

stackbegin = []
stackend = []

priorities={
  'double':5,
  'float':4,
  'long':3,
  'int':2,
  'char':1,
  'boolean':0
}

def highest_prior(lhs_type, rhs_type):
  return lhs_type if priorities[lhs_type]>priorities[rhs_type] else rhs_type

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

    def itr(self, elem, parent, payload = None, given_name = None):
        
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
                elem.itr(i, elem.parent, None, given_name=f"switch_case_{i.cases[0].value}")
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
                    else:
                        type = j.type
                    parameters[j.variable.name] = {'type': type, 'is_array': is_array, 'dimensions': dims, 'arr_size' : arr_size}
                    
                elem.methods[i.name] = {'n_parameters' : len(i.parameters), 'parameters' : parameters, 'return_type' : i.return_type}

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

                    elem.symb[name] = {'type': type, 'is_array': is_array, 'dimensions': dims, 'arr_size' : arr_size}

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
        else: print("Parent:", elem.parent)
        print("Scope:", elem.scope)
        print("Classes:", elem.classes)
        print("Methods:", elem.methods)
        print("Symbols:", elem.symb)

class ScopeField(BaseClass):
    pass

class CompilationUnit(BaseClass):

    def __init__(self, package_declaration=None, import_declarations=None, type_declarations=None):
        super(CompilationUnit, self).__init__()
        self._fields = ['package_declaration', 'import_declarations', 'type_declarations']
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
        ST.insert_in_sym_table(idName=name, idType='class', modifiers=modifiers, scope=parent_scope)
        ST.end_scope()
        stackbegin.pop()
        stackend.pop()

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

        if isinstance(self.type, Type):
            if isinstance(self.type.name, Name):
                type_ = self.type.name.value
            else:
                type_ = self.type.name
            if self.type.dimensions > 0:
                is_array = True
                type=type.name
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
            
                ST.insert_in_sym_table(idName=name, idType=type_, is_array=is_array, dims=dims, arr_size=arr_size, modifiers=modifiers)

class MethodDeclaration(ScopeField):

    def __init__(self, name, modifiers=None, parameters=None, return_type='void', body=None, type_parameters=None):
        super(MethodDeclaration, self).__init__()
        self._fields = ['name', 'modifiers', 'parameters', 'return_type', 'body', 'type_parameters']
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
            else:
                type = j.type
            params.append({'name' : j.variable.name, 'type': type, 'is_array': is_array, 'dims' : dims})
                    
        parent_scope = ST.get_parent_scope()
        ST.insert_in_sym_table(idName=name, idType='function', is_func=True, args=params, modifiers=modifiers, return_type=return_type, scope=parent_scope)


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
            else:
                type = j.type
            params.append({'name' : j.variable.name, 'type': type})

        parent_scope = ST.get_parent_scope()
        ST.insert_in_sym_table(name, idType='function', is_func=True, args=params, modifiers=modifiers, scope=parent_scope)
        ST.end_scope()
        stackbegin.pop()
        stackend.pop()

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
        self._fields = ['operator', 'lhs', 'rhs','type']
        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs
        self.type = None

class Assignment(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        if lhs.type!=rhs.type:
            if lhs.type in ['int','double','long','float','char'] and rhs.type in ['int','double','long','float','char'] and operator in ['=','+=','-=','*=','/=','&=','|=','^=','%=','<<=','>>=','>>>='] :
                self.type = highest_prior(lhs.type,rhs.type)
            else :
                print("Type mismatch in assignment.")
                print(lhs,rhs)


## BG start

class Conditional(Expression):

    def __init__(self, predicate, if_true, if_false):
        super(self.__class__, self).__init__()
        self._fields = ['predicate', 'if_true', 'if_false','type']
        parent_scope = ST.get_parent_scope()
        self.predicate = predicate
        self.if_true = if_true
        self.if_false = if_false

        if predicate.type in ['int','float','bool','long','double'] and if_true.type == if_false.type:
            self.type = if_true.type
        elif if_true.type not in ['int','float','bool','long','double'] or if_false.type not in ['int','float','bool','long','double'] :
            print("Type error in conditional expression.") 

class ConditionalOr(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        self.type = 'bool'

class ConditionalAnd(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        self.type = 'bool'

class Or(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        if lhs.type in ['int','char','long','bool'] and rhs.type in ['int','char','long','bool']:
            self.type = highest_prior(lhs.type,rhs.type)
        else:
            print("Error in Or operator operand types.")


class Xor(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        if lhs.type in ['int','char','long','bool'] and rhs.type in ['int','char','long','bool']:
            self.type = highest_prior(lhs.type,rhs.type)
        else:
            print("Error in Xor operator operand types.")


class And(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        if lhs.type in ['int','char','long','bool'] and rhs.type in ['int','char','long','bool']:
            self.type = highest_prior(lhs.type,rhs.type)
        else:
            print("Error in And operator operand types.")


class Equality(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        if lhs.type in ['int','char','long','bool','float','double'] and rhs.type in ['int','char','long','bool','float','double']:
            self.type = 'bool'
        else:
            print("Error in == operator operand types.")


class Relational(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        if lhs.type in ['int','char','long','bool','float','double'] and rhs.type in ['int','char','long','bool','float','double']:
            self.type = 'bool'
        else:
            print("Error in relational operator operand types.")
            # print(lhs,rhs)


class Shift(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        if lhs.type in ['int','char','long'] and rhs.type in ['int','char','long']:
            self.type = highest_prior(lhs.type,rhs.type)
        else:
            print("Error in Shift operator operand types.")


class Additive(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        if lhs.type in ['int','char','long','bool','float','double'] and rhs.type in ['int','char','long','bool','float','double']:
            self.type = highest_prior(lhs.type,rhs.type)
        else:
            print("Error in additive operator operand types.")


class Multiplicative(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        if lhs.type in ['int','char','long','bool','float','double'] and rhs.type in ['int','char','long','bool','float','double']:
            self.type = highest_prior(lhs.type,rhs.type)
        else:
            print("Error in multiplicative operator operand types.")


class Unary(Expression):

    def __init__(self, sign, expression):
        super(Unary, self).__init__()
        self._fields = ['sign', 'expression','type']
        self.sign = sign
        self.expression = expression
        self.type = expression.type

class Cast(Expression):

    def __init__(self, target, expression):
        super(Cast, self).__init__()
        self._fields = ['target', 'expression','type']
        self.target = target
        self.expression = expression
        self.type = target.name

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
        self._fields = ['name', 'arguments', 'type_arguments', 'target','type']
        a=name
        if type(name)!=str:
            a = name.value
        temp = ST.curr_scope
        temp_table = ST.scope_and_table_map[ST.curr_scope]
        f_type=None
        if '.' in a:
            a = a.split(".")
            for var in a:
                #print(var,ST.curr_scope)
                if f_type in ['int','float','bool','char','long','double']:
                    print("primitive type")
                if ST.lookup(var) == None and ST.lookup(var+'_'+ST.curr_scope,is_func=True) == None:
                    # print(f"Current Scope: {ST.curr_scope}")
                    print("Variable/Function",var, "not declared in current scope")
                    break
                elif ST.lookup(var) != None and ST.lookup(var)['type'] not in ['int','float','bool','char','long','double']:
                    if 'private' in ST.lookup(var)['modifiers']:
                        print(f"Tried to access a 'private' variable '{var}' from outside")
                        break
                    k = ST.lookup(var)['type']
                    print(var, k)
                    ST.curr_scope = k
                    ST.curr_sym_table = ST.scope_and_table_map[ST.curr_scope]
                    f_type = k
                elif ST.lookup(var+'_'+ST.curr_scope,is_func=True) != None:
                    if 'private' in ST.lookup(var+'_'+ST.curr_scope,is_func=True)['modifiers']:
                        print(f"Tried to access a 'private' function '{var}' from outside")
                        break
                    t=ST.curr_scope
                    ST.curr_scope = ST.lookup(var+'_'+ST.curr_scope,is_func=True)['name']
                    f_type = ST.lookup(var+'_'+t,is_func=True)['return_type']
                    ST.curr_sym_table = ST.scope_and_table_map[ST.curr_scope]
                elif ST.lookup(var) != None and ST.lookup(var)['type'] in ['int','float','bool','char','long','double']:
                    if 'private' in ST.lookup(var)['modifiers']:
                        print(f"Tried to access a 'private' variable '{var}' from outside")
                        break
                    f_type = ST.lookup(var)['type']
                    
            self.type = f_type
            name.value = var

        # print(ST.curr_scope)
        if arguments is None:
            arguments = []
        self.name = name
        self.arguments = arguments
        self.target = target
        self.type=None
        self.type_arguments=type_arguments
        try:
            #print(name.value + '_' + ST.curr_scope)
            if ST.lookup(ST.curr_scope,is_func=True) is None:
                print("Not a function")
            else :
                n_params = ST.lookup(ST.curr_scope,is_func=True)['n_params'] 
                self.type = ST.lookup(ST.curr_scope,is_func=True)['return_type'] 
                params = ST.lookup(ST.curr_scope,is_func=True)['params'] 
                if n_params!=len(arguments) :
                    print('Incorrect number of Arguements')
                else :
                    for i in range(len(arguments)):
                        if arguments[i].type != params[i]['type']:
                            print('Type of method arguement not correct')
        except:
            pass
        
        ST.curr_scope = temp
        ST.curr_sym_table = temp_table

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

        if expression.type not in ['int','long','bool','char']:
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
        self._fields = ['result']
        self.result = result

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
        self._fields = ['type', 'arguments', 'body']
        if arguments is None:
            arguments = []
        if body is None:
            body = []
        self.type = type
        self.arguments = arguments
        self.body = body

class FieldAccess(Expression):

    def __init__(self, name, target):
        super(FieldAccess, self).__init__()
        self._fields = ['name', 'target','type']
        self.name = name
        self.target = target
        self.type = None
        
        if target == 'this':
            self.type = name.type



# TODO array index out of range check
class ArrayAccess(Expression):

    def __init__(self, index, target):
        super(ArrayAccess, self).__init__()
        self._fields = ['index', 'target','type','depth','dimension']
        self.index = index
        self.target = target
        self.type = target.type
        if index.type not in ['int','long']:
            print('Array index not of type int')
        
        #while ST.lookup(target) is not None:
        #   target=target.target

        if target.__class__ == ArrayAccess:
            self.depth = target.depth + 1
            self.dimension = target.dimension
        else:
            self.depth = 1
            value = ST.lookup(target.value)
            self.dimension = value['dims']
        if self.depth > self.dimension:
            print("More than allowed dimension accessed")
        

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
        self._fields = ['value','type']
        self.value = value
        if value[0] == "'":
            self.type = 'char'
        elif self.value.find('.') == 1:
            self.type = 'double'
        else:
            self.type = 'int'

class Name(BaseClass):

    def __init__(self, value):
        super(Name, self).__init__()
        self._fields = ['value','type']
        self.value = value
        self.type = None

        if ST.lookup(value) == None and ST.lookup(value+'_'+ST.curr_scope,is_func=True) == None:
            print(ST.print_scope(ST.get_parent_scope()))
            print("Variable/Function",value, "not declared in current scope")
        elif ST.lookup(value) != None:
            self.type = ST.lookup(value)['type']
        else:
            self.type = ST.lookup(value+'_'+ST.curr_scope,is_func=True)['type'] 

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
            #print(a)
            for var in a:
                print(var,ST.curr_scope)
                if f_type in ['int','float','bool','char','long','double']:
                    print("primitive type")
                if ST.lookup(var) == None and ST.lookup(var+'_'+ST.curr_scope,is_func=True) == None:
                    print("Variable/Function",var, "not declared in current scope")
                    break
                elif ST.lookup(var) != None and ST.lookup(var)['type'] not in ['int','float','bool','char','long','double']:
                    if 'private' in ST.lookup(var)['modifiers']:
                        print(f"Tried to access a 'private' variable '{var}' from outside")
                        break
                    k = ST.lookup(var)['type']
                    ST.curr_scope = k
                    ST.curr_sym_table = ST.scope_and_table_map[ST.curr_scope]
                    f_type = k
                elif ST.lookup(var+'_'+ST.curr_scope,is_func=True) != None:
                    if 'private' in ST.lookup(var+'_'+ST.curr_scope,is_func=True)['modifiers']:
                        print(f"Tried to access a 'private' function '{var}' from outside")
                        break
                    t=ST.curr_scope
                    ST.curr_scope = ST.lookup(var+'_'+ST.curr_scope,is_func=True)['name']
                    f_type = ST.lookup(var+'_'+t,is_func=True)['return_type']
                    ST.curr_sym_table = ST.scope_and_table_map[ST.curr_scope]
                elif ST.lookup(var) != None and ST.lookup(var)['type'] in ['int','float','bool','char','long','double']:
                    if 'private' in ST.lookup(var)['modifiers']:
                        print(f"Tried to access a 'private' variable '{var}' from outside")
                        break
                    f_type = ST.lookup(var)['type']
                    
            ST.curr_scope = temp
            ST.curr_sym_table = temp_table
            self.type = f_type
                
                    
                




class ExpressionStatement(Statement):
    def __init__(self, expression):
        super(ExpressionStatement, self).__init__()
        self._fields = ['expression']
        self.expression = expression
