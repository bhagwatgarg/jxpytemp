widths = {'int':4, 'float':8, 'short':4, 'long':8, 'double':8, 'char':1}
count = -1
from new_sym_table import ScopeTable

ST=ScopeTable()
# all_types=

stackbegin = []
stackend = []

# Base node
import lexer
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

class SourceElement(object):
    '''
    A SourceElement is the base class for all elements that occur in a Java
    file parsed by plyj.
    '''

    def __init__(self):
        super(SourceElement, self).__init__()
        self._fields = []
        self.width = 0
        self.offset = 0
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

    def accept(self, visitor):
        """
        default implementation that visit the subnodes in the order
        they are stored in self_field
        """
        curr_offset = 0
        class_name = self.__class__.__name__
        visit = getattr(visitor, 'visit_' + class_name)
        if visit(self):
            for f in self._fields:
                field = getattr(self, f)
                if field:
                    if isinstance(field, list):
                        for elem in field:
                            if isinstance(elem, SourceElement):
                                elem.accept(visitor)
                    elif isinstance(field, SourceElement):
                        field.accept(visitor)
        getattr(visitor, 'leave_' + class_name)(self)

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

class ScopeField(SourceElement):
    pass

class CompilationUnit(SourceElement):

    def __init__(self, package_declaration=None, import_declarations=None,
                 type_declarations=None):
        super(CompilationUnit, self).__init__()
        self._fields = [
            'package_declaration', 'import_declarations', 'type_declarations']
        if import_declarations is None:
            import_declarations = []
        if type_declarations is None:
            type_declarations = []
        self.package_declaration = package_declaration
        self.import_declarations = import_declarations
        self.type_declarations = type_declarations

class PackageDeclaration(SourceElement):

    def __init__(self, name, modifiers=None):
        super(PackageDeclaration, self).__init__()
        self._fields = ['name', 'modifiers']
        if modifiers is None:
            modifiers = []
        self.name = name
        self.modifiers = modifiers        


class ImportDeclaration(SourceElement):

    def __init__(self, name, static=False, on_demand=False):
        super(ImportDeclaration, self).__init__()
        self._fields = ['name', 'static', 'on_demand']
        self.name = name
        self.static = static
        self.on_demand = on_demand


class ClassDeclaration(ScopeField):

    def __init__(self, name, body, modifiers=None, type_parameters=None,
                 extends=None, implements=None):
        super(ClassDeclaration, self).__init__()
        self._fields = ['name', 'body', 'modifiers',
                        'type_parameters', 'extends', 'implements']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if implements is None:
            implements = []
        self.name = name
        self.body = body
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extends = extends
        self.implements = implements

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

class ConstructorDeclaration(ScopeField):

    def __init__(self, name, block, modifiers=None, type_parameters=None,
                 parameters=None, throws=None):
        super(ConstructorDeclaration, self).__init__()
        self._fields = ['name', 'block', 'modifiers',
                        'type_parameters', 'parameters', 'throws']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if parameters is None:
            parameters = []
        self.name = name
        self.block = block
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.parameters = parameters
        self.throws = throws

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

class EmptyDeclaration(SourceElement):
    pass

class FieldDeclaration(SourceElement):

    def __init__(self, type, variable_declarators, modifiers=None):
        super(FieldDeclaration, self).__init__()
        self._fields = ['type', 'variable_declarators', 'modifiers']
        if modifiers is None:
            modifiers = []
        self.type = type
        self.variable_declarators = variable_declarators
        self.modifiers = modifiers

        type_ = ""
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

    def __init__(self, name, modifiers=None, type_parameters=None,
                 parameters=None, return_type='void', body=None, abstract=False,
                 extended_dims=0, throws=None):
        super(MethodDeclaration, self).__init__()
        self._fields = ['name', 'modifiers', 'type_parameters', 'parameters',
                        'return_type', 'body', 'abstract', 'extended_dims',
                        'throws']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if parameters is None:
            parameters = []
        self.name = name
        self.modifiers = modifiers
        self.parameters = parameters
        self.return_type = return_type
        self.body = body

        

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
        ST.insert_in_sym_table(idName=name, idType='function', is_func=True, args=params, modifiers=modifiers, return_type=return_type, scope=parent_scope)
        ST.end_scope()
        stackbegin.pop()
        stackend.pop()

class FormalParameter(SourceElement):

    def __init__(self, variable, type, modifiers=None, vararg=False):
        super(FormalParameter, self).__init__()
        self._fields = ['variable', 'type', 'modifiers', 'vararg']
        if modifiers is None:
            modifiers = []
        self.variable = variable
        self.type = type
        self.modifiers = modifiers
        self.vararg = vararg


class Variable(SourceElement):

    def __init__(self, name, dimensions=0):
        super(Variable, self).__init__()
        self._fields = ['name', 'dimensions']
        self.name = name
        self.dimensions = dimensions

class VariableDeclarator(SourceElement):

    def __init__(self, variable, initializer=None):
        super(VariableDeclarator, self).__init__()
        self._fields = ['variable', 'initializer']
        self.variable = variable
        self.initializer = initializer

class Type(SourceElement):

    def __init__(self, name, type_arguments=None, enclosed_in=None,
                 dimensions=0):
        super(Type, self).__init__()
        self._fields = ['name', 'type_arguments', 'enclosed_in', 'dimensions']
        if type_arguments is None:
            type_arguments = []
        self.name = name
        self.type_arguments = type_arguments
        self.enclosed_in = enclosed_in
        self.dimensions = dimensions

class Expression(SourceElement):

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

class Assignment(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        if lhs.type in ['int','double','long','float','char'] and rhs.type in ['int','double','long','float','char'] and operator in ['=','+=','-=','*=','/=','&=','|=','^=','%=','<<=','>>=','>>>='] :
            self.type = highest_prior(lhs.type,rhs.type)
        else :
            print("Type mismatch in assignment.")



## BG start

class Conditional(Expression):

    def __init__(self, predicate, if_true, if_false):
        super(self.__class__, self).__init__()
        self._fields = ['predicate', 'if_true', 'if_false']
        self.predicate = predicate
        self.if_true = if_true
        self.if_false = if_false

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

# Delete
#class InstanceOf(BinaryExpression):
#    pass


class Relational(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        if lhs.type in ['int','char','long','bool','float','double'] and rhs.type in ['int','char','long','bool','float','double']:
            self.type = 'bool'
        else:
            print("Error in relational operator operand types.")


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
            print("Error in relational operator operand types.")


class Multiplicative(BinaryExpression):
    def __init__(self, operator, lhs, rhs):
        super().__init__(operator, lhs, rhs)
        if lhs.type in ['int','char','long','bool','float','double'] and rhs.type in ['int','char','long','bool','float','double']:
            self.type = highest_prior(lhs.type,rhs.type)
        else:
            print("Error in relational operator operand types.")


class Unary(Expression):

    def __init__(self, sign, expression):
        super(Unary, self).__init__()
        self._fields = ['sign', 'expression']
        self.sign = sign
        self.expression = expression

class Cast(Expression):

    def __init__(self, target, expression):
        super(Cast, self).__init__()
        self._fields = ['target', 'expression']
        self.target = target
        self.expression = expression


class Statement(SourceElement):
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

class ArrayInitializer(SourceElement):
    def __init__(self, elements=None):
        super(ArrayInitializer, self).__init__()
        self._fields = ['elements']
        if elements is None:
            elements = []
        self.elements = elements


class MethodInvocation(Expression):
    def __init__(self, name, arguments=None, type_arguments=None, target=None):
        super(MethodInvocation, self).__init__()
        self._fields = ['name', 'arguments', 'type_arguments', 'target']
        if arguments is None:
            arguments = []
        if type_arguments is None:
            type_arguments = []
        self.name = name
        self.arguments = arguments
        self.type_arguments = type_arguments
        self.target = target

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

class SwitchCase(SourceElement):

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
    """An explicit invocations of a class's constructor.

    This is a variant of either this() or super(), NOT a "new" expression.
    """

    def __init__(self, name, target=None, type_arguments=None, arguments=None):
        super(ConstructorInvocation, self).__init__()
        self._fields = ['name', 'target', 'type_arguments', 'arguments']
        if type_arguments is None:
            type_arguments = []
        if arguments is None:
            arguments = []
        self.name = name
        self.target = target
        self.type_arguments = type_arguments
        self.arguments = arguments

class InstanceCreation(Expression):

    def __init__(self, type, type_arguments=None, arguments=None, body=None,
                 enclosed_in=None):
        super(InstanceCreation, self).__init__()
        self._fields = [
            'type', 'type_arguments', 'arguments', 'body', 'enclosed_in']
        if type_arguments is None:
            type_arguments = []
        if arguments is None:
            arguments = []
        if body is None:
            body = []
        self.type = type
        self.type_arguments = type_arguments
        self.arguments = arguments
        self.body = body
        self.enclosed_in = enclosed_in

class FieldAccess(Expression):

    def __init__(self, name, target):
        super(FieldAccess, self).__init__()
        self._fields = ['name', 'target']
        self.name = name
        self.target = target

# TODO array index out of range check
class ArrayAccess(Expression):

    def __init__(self, index, target):
        super(ArrayAccess, self).__init__()
        self._fields = ['index', 'target']
        self.index = index
        self.target = target

        if index.type not in ['int','long']:
            print('Array index not of type int')


class ArrayCreation(Expression):

    def __init__(self, type, dimensions=None, initializer=None):
        super(ArrayCreation, self).__init__()
        self._fields = ['type', 'dimensions', 'initializer']
        if dimensions is None:
            dimensions = []
        self.type = type
        self.dimensions = dimensions
        self.initializer = initializer


class Literal(SourceElement):

    def __init__(self, value):
        super(Literal, self).__init__()
        self._fields = ['value']
        self.value = value


class Name(SourceElement):

    def __init__(self, value):
        super(Name, self).__init__()
        self._fields = ['value','type']
        self.value = value
        
        global ST
        if ST.lookup(value) == None:
            print("Variable ",value, "not declared in current scope")
        else:
            self.type = ST.lookup(value)['idType']

        #lookup for name in symbol table.
        #if name present in table in current scope
        #then no problem else undeclared variable.

    def append_name(self, name):
        try:
            self.value = self.value + '.' + name.value
        except:
            self.value = self.value + '.' + name


class ExpressionStatement(Statement):
    def __init__(self, expression):
        super(ExpressionStatement, self).__init__()
        self._fields = ['expression']
        self.expression = expression


class Visitor(object):

    def __init__(self, verbose=False):
        self.verbose = verbose

    def __getattr__(self, name):
        if not (name.startswith('visit_') or name.startswith('leave_')):
            raise AttributeError('name must start with visit_ or leave_ but was {}'
                                 .format(name))

        def f(element):
            if self.verbose:
                msg = 'unimplemented call to {}; ignoring ({})'
                print(msg.format(name, element))
            return True
        return f
