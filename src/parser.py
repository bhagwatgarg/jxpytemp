import sys
import ply.yacc as yacc
import lexer
from model import *

import pydot
import os

graph = pydot.Dot("my_graph", graph_type="digraph", bgcolor="white")
node_num=0

breaks = []
continues = []

def generate_ast(p, parent=None, arr_name=None):
    global graph, node_num
    curr_obj=p
    curr_class=None
    curr_val=str(node_num)
    if p==None: return
    try:
        curr_class=curr_obj.__class__
    except:
        # it is a terminal
        # print(f"Terminal: {curr_obj}")
        return
    if type(p)==type([]):
        if len(p)==0: return
        if arr_name==None:
            arr_name="None"
            # raise Exception(f"ERROR! {curr_class.__name__} arrname not given")
            print(f"ERROR! {curr_class.__name__} arrname not given")
        graph.add_node(pydot.Node((curr_val), label=arr_name))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        for i in p: generate_ast(i, curr_val)
        return

    if curr_class==CompilationUnit:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        generate_ast(p.package_declaration, curr_val)
        generate_ast(p.import_declarations, curr_val, arr_name='ImportDeclarations')
        generate_ast(p.type_declarations, curr_val, arr_name='TypeDeclarations')

    elif curr_class in [PackageDeclaration]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.name, curr_val)

    elif curr_class in [ImportDeclaration]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast('.'.join(p.name), curr_val)

    elif curr_class in [ClassDeclaration]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.name, curr_val)
        generate_ast(p.body, curr_val, arr_name='Body')
        generate_ast(p.modifiers, curr_val, arr_name='Modifiers')

    elif curr_class in [ClassInitializer]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.block, curr_val)
        generate_ast(p.static, curr_val)
    
    elif curr_class in [FieldDeclaration]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.type, curr_val)
        generate_ast(p.variable_declarators, curr_val, arr_name='VariableDeclarators')
        generate_ast(p.modifiers, curr_val, arr_name='Modifiers')

    elif curr_class in [MethodDeclaration]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.name, curr_val)
        generate_ast(p.modifiers, curr_val, arr_name='Modifiers')
        generate_ast(p.parameters, curr_val, arr_name='Parameters')
        generate_ast(p.return_type, curr_val)
        generate_ast(p.body, curr_val, arr_name='Body')

    elif curr_class in [ConstructorDeclaration]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.name, curr_val)
        generate_ast(p.block, curr_val)
        generate_ast(p.modifiers, curr_val, arr_name='Modifiers')
        generate_ast(p.parameters, curr_val, arr_name='Parameters')

    elif curr_class in [FormalParameter]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.variable, curr_val)
        generate_ast(p.type, curr_val)

    elif curr_class in [Variable]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.name, curr_val)
        generate_ast(p.dimensions, curr_val)

    elif curr_class in [VariableDeclarator]:
        graph.add_node(pydot.Node((curr_val), label='='))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.variable, curr_val)
        generate_ast(p.initializer, curr_val)
    
    elif curr_class in [Type]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.dimensions, curr_val)

    elif issubclass(curr_class, BinaryExpression):
        # graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        graph.add_node(pydot.Node((curr_val), label=str(p.operator)))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.lhs, curr_val)
        generate_ast(p.rhs, curr_val)

    elif curr_class in [Conditional]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.predicate, curr_val)
        generate_ast(p.if_true, curr_val)
        generate_ast(p.if_false, curr_val)

    elif curr_class in [Unary]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.sign, curr_val)
        generate_ast(p.expression, curr_val)

    elif curr_class in [Cast]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.target, curr_val)
        generate_ast(p.expression, curr_val)

    elif curr_class in [Block]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.statements, curr_val, arr_name='Statements')


    elif curr_class in [ArrayInitializer]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.elements, curr_val, arr_name='Elements')

    elif curr_class in [MethodInvocation]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.name, curr_val)
        generate_ast(p.arguments, curr_val, arr_name='Arguments')
        generate_ast(p.target, curr_val)

    elif curr_class in [IfThenElse]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.predicate, curr_val)
        generate_ast(p.if_true, curr_val)
        generate_ast(p.if_false, curr_val)

    elif curr_class in [While]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.predicate, curr_val)
        generate_ast(p.body, curr_val, arr_name='Body')
    
    elif curr_class in [For]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.init, curr_val, arr_name='Init')
        generate_ast(p.predicate, curr_val, arr_name='Predicate')
        generate_ast(p.update, curr_val, arr_name='Update')
        generate_ast(p.body, curr_val, arr_name='Body')

    elif curr_class in [Switch]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.expression, curr_val)
        generate_ast(p.body, curr_val, arr_name='Body')
    
    elif curr_class in [SwitchCase]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.cases, curr_val, arr_name='Cases')
        generate_ast(p.body, curr_val, arr_name='Body')
    
    elif curr_class in [DoWhile]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.predicate, curr_val)
        generate_ast(p.body, curr_val, arr_name='Body')

    elif curr_class in [Continue, Break]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.label, curr_val)

    elif curr_class in [Return]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.result, curr_val)

    elif curr_class in [ConstructorInvocation]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.name, curr_val)
        generate_ast(p.target, curr_val)
        generate_ast(p.arguments, curr_val, arr_name='Arguments')

    elif curr_class in [FieldAccess]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.name, curr_val)
        generate_ast(p.target, curr_val)

    elif curr_class in [ArrayAccess]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.index, curr_val)
        generate_ast(p.target, curr_val)

    elif curr_class in [ArrayCreation]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.type, curr_val)
        generate_ast(p.dimensions, curr_val)
        generate_ast(p.initializer, curr_val)

    elif curr_class in [ExpressionStatement]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
        generate_ast(p.expression, curr_val)

    elif curr_class in [EmptyDeclaration, Expression]:
        graph.add_node(pydot.Node((curr_val), label=curr_class.__name__))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))

    elif curr_class in [Literal, Name]:
        graph.add_node(pydot.Node((curr_val), label=curr_obj.value))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
    elif curr_class in [str, int, bool]:
        graph.add_node(pydot.Node((curr_val), label=curr_obj))
        node_num+=1
        graph.add_edge(pydot.Edge(str(parent), (curr_val)))
    else:
        pass

#   CompilationUnit().

def p_Goal(p):
    '''Goal : CompilationUnit'''
    p[0] = p[1]
    # print(p[0])
    ST.print_scope_table()
    generate_ast(p[0])
    prefix='.'
    graph.write(prefix+'/graph.dot')
    os.system(f"dot -Tpng '{prefix}/graph.dot' -o '{prefix}/graph.png'")
    # os.system(f"sfdp -x -Tpng '{prefix}/graph.dot' > '{prefix}/graph.png'")
    # os.system(f"sfdp -x -Goverlap=scale -Tpng '{prefix}/graph.dot' > '{prefix}/graph.png'")
    # graph.write_png(f'{prefix}graph.png')
    # os.system(f"xdg-open '{prefix}/graph.png'")

def p_Literal(p):
    ''' Literal : DECIMAL_LITERAL 
    | HEX_LITERAL 
    | BINARY_LITERAL 
    | FLOAT_LITERAL 
    | BOOL_LITERAL 
    | CHAR_LITERAL 
    | STRING_LITERAL 
    | NULL
    '''
    p[0] = Literal(p[1])

def p_Type(p):
    ''' Type : PrimitiveType
    | ReferenceType
    '''
    p[0] = p[1]

def p_PrimitiveType(p):
    ''' PrimitiveType : NumericType
    | BOOLEAN
    '''
    p[0] = p[1]

def p_NumericType(p):
    ''' NumericType : IntegralType
    | FloatingPointType
    '''
    p[0] = p[1]

def p_IntegralType(p):
    ''' IntegralType : BYTE
    | SHORT
    | INT
    | LONG
    | CHAR
    '''
    p[0] = p[1]

def p_FloatingPointType(p):
    ''' FloatingPointType : FLOAT
    | DOUBLE
    '''
    p[0] = p[1]

def p_ReferenceType(p):
    ''' ReferenceType : ArrayType
    | ClassType
    '''
    p[0] = p[1]

def p_ClassType(p):
    '''
    ClassType : Name
    '''
    p[0] = p[1]

def p_ArrayType(p):
    ''' ArrayType : PrimitiveType Dims
    | Name Dims
    '''
    p[0] = Type(p[1], dimensions = p[2])

def p_Name(p):
    ''' Name : SimpleName
    | QualifiedName'''
    p[0] = p[1]

def p_SimpleName(p):
    ''' SimpleName : IDENTIFIER'''
    p[0] = Name(p[1])

def p_QualifiedName(p):
    ''' QualifiedName : Name DOT IDENTIFIER'''
    p[1].append_name(p[3])
    p[0] = p[1]

def p_CompilationUnit(p):
    '''
    CompilationUnit : PackageDeclaration ImportDeclarations TypeDeclarations
    | PackageDeclaration ImportDeclarations
    | PackageDeclaration
    '''
    if len(p)==4 :
        p[0] = CompilationUnit(package_declaration=p[1], import_declarations=p[2], type_declarations=p[3])
    elif len(p)==3 :
        p[0] = CompilationUnit(package_declaration=p[1], import_declarations=p[2])
    else :
        p[0] = CompilationUnit(package_declaration=p[1])

def p_CompilationUnit2(p):
    '''
    CompilationUnit : PackageDeclaration TypeDeclarations
    | ImportDeclarations
    '''
    if len(p)==3:
        p[0] = CompilationUnit(package_declaration=p[1], type_declarations=p[2])
    else :
        p[0] = CompilationUnit(import_declarations=p[1])

def p_CompilationUnit3(p):
    '''
    CompilationUnit :  ImportDeclarations TypeDeclarations
    | TypeDeclarations
    '''
    if len(p)==3:
        p[0] = CompilationUnit(import_declarations=p[1], type_declarations=p[2])
    else :
        p[0] = CompilationUnit(type_declarations=p[1])

def p_ImportDeclarations(p):
    '''
    ImportDeclarations : ImportDeclaration
    | ImportDeclarations ImportDeclaration
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_TypeDeclarations(p):
    '''
    TypeDeclarations : TypeDeclaration
    | TypeDeclarations TypeDeclaration
    '''
    if len(p) == 2: p[0] = [p[1]]
    else: p[0] = p[1] + [p[2]]

def p_PackageDeclaration(p):
    '''
    PackageDeclaration : PACKAGE IDENTIFIER SEMI
    '''
    p[0] = PackageDeclaration(p[2])

def p_ImportDeclaration(p):
    '''
    ImportDeclaration : SingleTypeImportDeclaration
    | TypeImportOnDemandDeclaration
    '''
    # print(p[1])
    p[0] = p[1]

def p_SingleTypeImportDeclaration(p):
    '''
    SingleTypeImportDeclaration : IMPORT import_identifier SEMI
    '''
    p[0] = ImportDeclaration(p[2])

def p_TypeImportOnDemandDeclaration(p):
    '''
    TypeImportOnDemandDeclaration : IMPORT import_identifier DOT MUL SEMI
    '''
    p[0] = ImportDeclaration(p[2], on_demand=True)

def p_import_identifier(p):
    '''
    import_identifier : import_identifier DOT IDENTIFIER
    | IDENTIFIER
    '''
    if len(p) == 2: p[0] = [p[1]]
    else: p[0] = p[1] + [p[3]]

def p_TypeDeclaration(p):
    '''
    TypeDeclaration : ClassDeclaration
    '''
    p[0] = p[1]

def p_TypeDeclaration2(p):
    '''
    TypeDeclaration : SEMI
    '''
    p[0] = EmptyDeclaration()

# split this according to titanium http://titanium.cs.berkeley.edu/doc/java-langspec-1.0/19.doc.html
def p_Modifiers(p):
    '''
    Modifiers : Modifier
    | Modifiers Modifier
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_Modifier(p):
    '''
    Modifier : STATIC
    | FINAL
    | PRIVATE
    | PROTECTED
    | PUBLIC
    '''
    p[0] = p[1]

def p_ClassDeclaration(p):
    '''
    ClassDeclaration : Modifiers CLASS IDENTIFIER decl_mark_2 ClassBody
    | CLASS IDENTIFIER decl_mark_2 ClassBody
    '''
    if len(p) == 6: p[0] = ClassDeclaration(name = p[3], body = p[5], modifiers = p[1])
    else: p[0] = ClassDeclaration(name = p[2], body = p[4])

def p_ClassBody(p):
    '''
    ClassBody : LBRACE RBRACE
    | LBRACE ClassBodyDeclarations RBRACE
    '''
    if len(p) == 3: p[0] = []
    else: p[0] = p[2]

def p_ClassBodyDeclarations(p):
    '''
    ClassBodyDeclarations : ClassBodyDeclaration
    | ClassBodyDeclarations ClassBodyDeclaration
    '''
    if len(p) == 2: p[0] = [p[1]]
    else: p[0] = p[1] + [p[2]]

def p_ClassBodyDeclaration(p):
    '''
    ClassBodyDeclaration : ClassMemberDeclaration
    | ConstructorDeclaration
    | StaticInitializer
    '''
    p[0] = p[1]

def p_ClassMemberDeclaration(p):
    '''
    ClassMemberDeclaration : FieldDeclaration
    | MethodDeclaration
    '''
    p[0] = p[1]

def p_FieldDeclaration(p):
    '''
    FieldDeclaration : Modifiers Type VariableDeclarators SEMI
    | Type VariableDeclarators SEMI
    '''
    if len(p) == 5: p[0] = FieldDeclaration(type = p[2], variable_declarators = p[3], modifiers = p[1])
    else: p[0] = FieldDeclaration(type = p[1], variable_declarators = p[2])

def p_VariableDeclarators(p):
    '''
    VariableDeclarators : VariableDeclarator
    | VariableDeclarators COMMA VariableDeclarator
    '''
    if len(p) == 2: p[0] = [p[1]]
    else: p[0] = p[1] + [p[3]]

def p_VariableDeclarator(p):
    '''
    VariableDeclarator : VariableDeclaratorId
    | VariableDeclaratorId ASSIGN VariableInitializer
    '''
    if len(p) == 2: p[0] = VariableDeclarator(p[1])
    else: p[0] = VariableDeclarator(p[1], initializer = p[3])

def p_VariableDeclaratorId(p):
    # made a change here
    '''
    VariableDeclaratorId : IDENTIFIER
    | IDENTIFIER Dims
    '''
    dims=0
    if len(p)==3: dims=p[2]
    p[0] = Variable(p[1], dimensions = dims)

def p_VariableInitializer(p):
    '''
    VariableInitializer : Expression
    | ArrayInitializer
    '''
    p[0] = p[1]

def p_MethodDeclaration(p):
    '''
    MethodDeclaration : MethodHeader MethodBody
    '''
    ST.end_scope()
    # stackbegin.pop()
    # stackend.pop()
    p[0]=p[1]
    # print(p[1])
    p[0].body=p[2]
    # TODO can have ST stuff in model for this
    # TODO
    # p[0] = MethodDeclaration(p[1]['name'], parameters=p[1]['parameters'],
    #                                  extended_dims=p[1]['extended_dims'], type_parameters=p[1]['type_parameters'],
    #                                  return_type=p[1]['type'], modifiers=p[1]['modifiers'], body=p[2])

# def p_MethodDeclMark(p):
#     '''
#     MethodDeclMark :
#     '''
#     p[0] = 


def p_MethodHeader(p):
    '''
    MethodHeader : Modifiers Type MethodDeclarator
    | Type MethodDeclarator
    '''
    var={}
    if len(p)==4:
        var = {'modifiers': p[1], 'type': p[2], 'name': p[3]['name'], 'parameters': p[3]['parameters']}
    else:
        var = {'type': p[1], 'name': p[2]['name'], 'modifiers':[], 'parameters': p[2]['parameters']}
    # p[0]=MethodDeclaration(p[-1]['name'], parameters = p[-1]['parameters'], return_type=p[-1]['type'], modifiers=p[-1]['modifiers'], body=None)
    
    params = []

    for j in var['parameters']:
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
                
    idName = var['name'] + "_" + ST.curr_scope

    for i in params:
        idName += "_" + i['type']
    
    var['name'] = idName

    ST.create_new_table(var['name'], scope_type="func")
    # print(f"table vreated: {var['name']}")
    # stackbegin.append(var['name'])
    # stackend.append(var['name'])
    p[0] = MethodDeclaration(var['name'], parameters = var['parameters'], return_type= var['type'], modifiers= var['modifiers'], body=None)
    # print(p[0], 'qwer')
    
    for j in var['parameters']:
        type = ""
        is_array = False
        dims = 0
        arr_size = []
        if isinstance(j.type, Type):
            # if j.name=='arr':
            #     print(j)
            if isinstance(j.type.name, Name):
                type = j.type.name.value
            else:
                type = j.type.name
            if j.type.dimensions > 0:
                is_array = True
                dims = j.type.dimensions
        else:
            type = j.type
            dims=j.variable.dimensions
            if dims>0:
                is_array=True
        ST.insert_in_sym_table(idName=j.variable.name, idType=type, is_func=False, is_array=is_array, dims=dims, arr_size=arr_size)


def p_MethodHeader2(p):
    '''
    MethodHeader : Modifiers VOID MethodDeclarator
    | VOID MethodDeclarator
    '''
    # print(f"Curr Scope: {ST.curr_scope}")
    var={}
    if len(p) == 4:
        var = {'modifiers': p[1], 'name': p[3]['name'], 'type':'void', 'parameters': p[3]['parameters']}
    else:
        var = {'name': p[2]['name'], 'type':'void', 'modifiers':[], 'parameters': p[2]['parameters']}
    
    params = []

    for j in var['parameters']:
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
                
    idName = var['name'] + "_" + ST.curr_scope

    for i in params:
        idName += "_" + i['type']
    
    var['name'] = idName
    
    ST.create_new_table(var['name'], scope_type="func")
    # print(f"table vreated: {var['name']}")
    # stackbegin.append(var['name'])
    # stackend.append(var['name'])
    p[0]=MethodDeclaration(var['name'], parameters = var['parameters'], return_type=var['type'], modifiers=var['modifiers'], body=None)
    # print(f"Curr Scope: {ST.curr_scope}")
    # print(var['parameters'])
    # print(ST.curr_scope)
    for j in var['parameters']:
        # print(j)
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
            dims=j.variable.dimensions
            if dims>0:
                is_array=True

        ST.insert_in_sym_table(idName=j.variable.name, idType=type, is_func=False, is_array=is_array, dims=dims, arr_size=arr_size)

def p_MethodDeclarator(p):
    '''
    MethodDeclarator : IDENTIFIER LPAREN RPAREN
    | IDENTIFIER LPAREN FormalParameterList RPAREN
    '''
    p[0]={}
    if len(p)==4:
        p[0]['name']=p[1]
        p[0]['parameters'] = []
    else :
        p[0]['name']=p[1]
        p[0]['parameters']=p[3]

    # if len(p) == 6:
    #     for j in p[4]:
    #         type = ""
    #         is_array = False
    #         dims = 0
    #         arr_size = []
    #         if isinstance(j.type, Type):
    #             if isinstance(j.type.name, Name):
    #                 type = j.type.name.value
    #             else:
    #                 type = j.type.name
    #             if j.type.dimensions > 0:
    #                 is_array = True
    #                 dims = j.type.dimensions
    #         else:
    #             type = j.type
    #         ST.insert_in_sym_table(idName=j.variable.name, idType=type, is_func=False, is_array=is_array, dims=dims, arr_size=arr_size)

def p_FormalParametersList(p):
    '''
    FormalParameterList : FormalParameter
    | FormalParameterList COMMA FormalParameter
    '''
    if len(p) == 2: p[0] = [p[1]]
    else: p[0] = p[1] + [p[3]]

def p_FormalParameter(p):
    '''
    FormalParameter : Type VariableDeclaratorId
    '''
    p[0] = FormalParameter(variable = p[2], type = p[1])

#def p_ClassTypeList(p):
#    '''
#    ClassTypeList : ClassType
#    | ClassTypeList COMMA ClassType
#    '''

def p_MethodBody(p):
    '''
    MethodBody : Block
    | SEMI
    '''
    p[0] = p[1]

def p_StaticInitializer(p):
    '''
    StaticInitializer : begin_scope STATIC Block end_scope
    '''
    p[0] = ClassInitializer(p[3], static = True)


### BG START

def p_ConstructorDeclaration(p):
    '''
    ConstructorDeclaration : Modifiers ConstructorDeclarator ConstructorBody
    | ConstructorDeclarator ConstructorBody
    '''
    modifiers, declarator, body=None, None, None
    if len(p)==4:
        modifiers=p[1]
        declarator=p[2]
        body=p[3]
    else:
        declarator=p[1]
        body=p[2]
    p[0]=ConstructorDeclaration(name=declarator['simple_name'].value, block=body['block_statements'], modifiers=modifiers, type_parameters=None, parameters=declarator['formal_parameter_list'], throws=None)

def p_ConstructorDeclarator(p):
    '''
    ConstructorDeclarator : SimpleName LPAREN decl_mark FormalParameterList RPAREN
    | SimpleName decl_mark LPAREN RPAREN
    '''
    param_list=[]       # empty list of params
    if len(p)==6:
        param_list=p[4]
    p[0]={
        'simple_name': p[1],
        'formal_parameter_list': param_list
    }

    if len(p) == 6:
        for j in p[4]:
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
            ST.insert_in_sym_table(idName=j.variable.name, idType=type, is_func=False, is_array=is_array, dims=dims, arr_size=arr_size)


def p_ConstructorBody(p):
    '''
    ConstructorBody :
    | LBRACE BlockStatements RBRACE
    | LBRACE RBRACE
    '''
    constructor_invocation, block_statements=None, None
    if len(p)==4:
        block_statements=p[2]
    elif len(p)==5:
        constructor_invocation=p[2]
        block_statements=p[3]
    p[0]={
        'explicit_constructor_invocation': constructor_invocation,
        'block_statements': block_statements
    }

def p_ExplicitConstructorInvocation(p):
    '''
    ExplicitConstructorInvocation : THIS LPAREN ArgumentList RPAREN SEMI
    | THIS LPAREN RPAREN SEMI
    '''
    arg_list=[]
    if len(p)==6: arg_list=p[3]
    p[0]={'argument_list': arg_list}

def p_ArrayInitializer(p):
    '''
    ArrayInitializer : LBRACE VariableInitializers RBRACE
    | LBRACE RBRACE
    '''
    variable_initializers=[]
    if len(p)==4: variable_initializers=p[2]
    p[0]=ArrayInitializer(variable_initializers)

def p_VariableInitializers(p):
    '''
    VariableInitializers : VariableInitializer
    | VariableInitializers COMMA VariableInitializer
    '''
    if len(p)==2: p[0]=[p[1]]
    else: p[0]=p[1]+[p[3]]

def p_Block(p):
    '''
    Block : LBRACE RBRACE
    | LBRACE BlockStatements RBRACE
    '''
    block_statements=None
    if len(p)==4: block_statements=p[2]
    p[0]=Block(statements=block_statements)

def p_BlockStatements(p):
    '''
    BlockStatements : BlockStatement
    | BlockStatements BlockStatement
    '''
    if len(p)==2: p[0]=[p[1]]
    else: p[0]=p[1]+[p[2]]

def p_BlockStatement(p):
    '''
    BlockStatement : LocalVariableDeclarationStatement
    | Statement
    '''
    p[0]=p[1]

def p_LocalVariableDeclarationStatement(p):
    '''
    LocalVariableDeclarationStatement : LocalVariableDeclaration SEMI
    '''
    p[0]=p[1]

def p_LocalVariableDeclaration(p):
    '''
    LocalVariableDeclaration : Type VariableDeclarators
    '''
    p[0]=VariableDeclaration(type=p[1], variable_declarators=p[2])

def p_Statement(p):
    '''
    Statement : StatementWithoutTrailingSubstatement
    | LabeledStatement
    | IfThenStatement
    | IfThenElseStatement
    | WhileStatement
    | ForStatement
    '''
    p[0]=p[1]

def p_StatementNoShortIf(p):
    '''
    StatementNoShortIf : StatementWithoutTrailingSubstatement
    | LabeledStatementNoShortIf
    | IfThenElseStatementNoShortIf
    | WhileStatementNoShortIf
    | ForStatementNoShortIf
    '''
    p[0]=p[1]

def p_StatementWithoutTrailingSubstatement(p):
    '''
    StatementWithoutTrailingSubstatement : Block
    | EmptyStatement
    | ExpressionStatement
    | SwitchStatement
    | DoStatement
    | BreakStatement
    | ContinueStatement
    | ReturnStatement
    '''
    p[0]=p[1]

def p_EmptyStatement(p):
    '''
    EmptyStatement : SEMI
    '''
    p[0]=Empty()

def p_LabeledStatement(p):
    '''
    LabeledStatement : IDENTIFIER COLON Statement
    '''
    p[3].label=p[1]
    p[0]=p[3]

def p_LabeledStatementNoShortIf(p):
    '''
    LabeledStatementNoShortIf : IDENTIFIER COLON StatementNoShortIf
    '''
    p[3].label=p[1]
    p[0]=p[3]

def p_ExpressionStatement(p):
    '''
    ExpressionStatement : StatementExpression SEMI
    '''
    p[0]=ExpressionStatement(expression=p[1])

def p_StatementExpression(p):
    '''
    StatementExpression : Assignment
    | PreIncrementExpression
    | PreDecrementExpression
    | PostIncrementExpression
    | PostDecrementExpression
    | MethodInvocation
    | ClassInstanceCreationExpression
    '''
    p[0]=p[1]

def p_IfThenStatement(p):
    '''
    IfThenStatement : IF begin_scope LPAREN Expression RPAREN Statement end_scope
    '''
    p[0]=IfThenElse(predicate=p[4], if_true=p[6])

def p_IfThenElseStatement(p):
    '''
    IfThenElseStatement : IF begin_scope LPAREN Expression RPAREN StatementNoShortIf end_scope ELSE begin_scope Statement end_scope
    '''
    p[0]=IfThenElse(predicate=p[4], if_true=p[6], if_false=p[10])

def p_IfThenElseStatementNoShortIf(p):
    '''
    IfThenElseStatementNoShortIf : IF begin_scope LPAREN Expression RPAREN StatementNoShortIf end_scope ELSE begin_scope StatementNoShortIf end_scope
    '''
    p[0]=IfThenElse(predicate=p[3], if_true=p[6], if_false=p[10])

def p_SwitchStatement(p):
    '''
    SwitchStatement : SWITCH LPAREN Expression RPAREN SwitchBlock
    '''
    p[0]=Switch(expression=p[3], switch_cases=p[5])

def p_SwitchBlock(p):
    '''
    SwitchBlock : LBRACE RBRACE
    | LBRACE SwitchBlockStatementGroups begin_scope SwitchLabels end_scope RBRACE
    | LBRACE SwitchBlockStatementGroups RBRACE
    '''
    if len(p)==3: p[0]=[]
    elif len(p)==4: p[0]=p[2]
    else: p[0]=p[2]+[SwitchCase(p[4])]

def p_SwitchBlock2(p):
    '''
    SwitchBlock : LBRACE begin_scope SwitchLabels end_scope RBRACE
    '''
    p[0]=[SwitchCase(p[3])]


def p_SwitchBlockStatementGroups(p):
    '''
    SwitchBlockStatementGroups : SwitchBlockStatementGroup
    | SwitchBlockStatementGroups SwitchBlockStatementGroup
    '''
    if len(p)==2: p[0]=[p[1]]
    else: p[0]=p[1]+[p[2]]

def p_SwitchBlockStatementGroup(p):
    '''
    SwitchBlockStatementGroup : begin_scope SwitchLabels BlockStatements end_scope
    '''
    p[0]=SwitchCase(cases=p[2], body=p[3])

def p_SwitchLabels(p):
    '''
    SwitchLabels : SwitchLabel
    | SwitchLabels SwitchLabel
    '''
    if len(p)==2: p[0]=[p[1]]
    else: p[0]=p[1]+[p[2]]

def p_SwitchLabel(p):
    '''
    SwitchLabel : CASE ConstantExpression COLON
    | DEFAULT COLON
    '''
    if len(p)==4: p[0]=p[2]
    else: p[0]='default'

def p_WhileStatement(p):
    '''
    WhileStatement : WHILE prep_fw_stack LPAREN begin_scope while_l1 Expression RPAREN while_l1 Statement end_scope while_l2
    '''
    p[0]=While(predicate=p[6], body=p[9])

    tac.backpatch(continues[-1], p[5])
    tac.backpatch(breaks[-1], p[11])
    
    tac.backpatch(p[6].truelist, p[8])
    tac.backpatch(p[6].falselist, p[11])

    continues.pop()
    breaks.pop()

def p_WhileStatementNoShortIf(p):
    '''
    WhileStatementNoShortIf : WHILE prep_fw_stack LPAREN begin_scope while_l1 Expression RPAREN while_l1 StatementNoShortIf end_scope while_l2
    '''
    p[0]=While(predicate=p[6], body=p[9])

    tac.backpatch(continues[-1], p[5])
    tac.backpatch(breaks[-1], p[11])
    
    tac.backpatch(p[6].truelist, p[8])
    tac.backpatch(p[6].falselist, p[11])

    continues.pop()
    breaks.pop()

def p_prep_fw_stack(p):
    '''
    prep_fw_stack : 
    '''
    continues.append([])
    breaks.append([])

def p_while_l1(p):
    '''
    while_l1 : 
    '''
    label = 'while_' + ST.make_label()
    p[0] = label
    tac.emit('label :', '', '', label)

def p_while_l2(p):
    '''
    while_l2 :
    '''
    label = 'while_' + ST.make_label()
    p[0] = label
    tac.emit('goto','', '', p[-6])
    tac.emit('label :', '', '', label)

def p_DoStatement(p):
    '''
    DoStatement : DO prep_fw_stack begin_scope dwhile_l1 Statement WHILE LPAREN dwhile_l1 Expression RPAREN SEMI end_scope dwhile_l2
    '''
    p[0]=DoWhile(predicate=p[9], body=p[5])

    tac.backpatch(continues[-1], p[8])
    tac.backpatch(breaks[-1], p[13])
    
    tac.backpatch(p[6].truelist, p[4])
    tac.backpatch(p[6].falselist, p[13])

    continues.pop()
    breaks.pop()

def p_dwhile_l1(p):
    '''
    dwhile_l1 : 
    '''
    label = 'dowhile_' + ST.make_label()
    p[0] = label
    tac.emit('label :', '', '', label)

def p_dwhile_l2(p):
    '''
    dwhile_l2 :
    '''
    label = 'dowhile_' + ST.make_label()
    p[0] = label
    tac.emit('goto','', '', p[-5])
    tac.emit('label :', '', '', label)

def p_ForStatement(p):
    '''
    ForStatement : FOR prep_fw_stack LPAREN begin_scope ForInit SEMI for_l1 Expression SEMI for_l1 ForUpdate for_l3 RPAREN for_l1 Statement end_scope for_l2
    | FOR prep_fw_stack LPAREN begin_scope SEMI for_l1 Expression SEMI for_l1 ForUpdate for_l3 RPAREN for_l1 Statement end_scope for_l2
    | FOR prep_fw_stack LPAREN begin_scope ForInit SEMI for_l1 SEMI for_l1 ForUpdate for_l3 RPAREN for_l1 Statement end_scope for_l2
    | FOR prep_fw_stack LPAREN begin_scope ForInit SEMI for_l1 Expression SEMI for_l1 for_l3 RPAREN for_l1 Statement end_scope for_l2
    | FOR prep_fw_stack LPAREN begin_scope ForInit SEMI for_l1 SEMI for_l1 for_l3 RPAREN for_l1 Statement end_scope for_l2
    | FOR prep_fw_stack LPAREN begin_scope SEMI for_l1 Expression SEMI for_l1 for_l3 RPAREN for_l1 Statement end_scope for_l2
    | FOR prep_fw_stack LPAREN begin_scope SEMI for_l1 SEMI for_l1 ForUpdate for_l3 RPAREN for_l1 Statement end_scope for_l2
    | FOR prep_fw_stack LPAREN begin_scope SEMI for_l1 SEMI for_l1 for_l3 RPAREN for_l1 Statement end_scope for_l2
    '''
    init, predicate, update, body, conts, brks, tl_jumps =None, None, None, None, None, None, None
    if len(p) == 18:
        init = p[5]
        predicate = p[8]
        update = p[11]
        body = p[15]
        conts = p[10]
        brks = p[17]
        tl_jumps = p[14]
    elif len(p) == 17:
        body = p[14]
        brks = p[16]
        tl_jumps = p[13]
        if p[5] ==';':
            predicate = p[7]
            update = p[10]
            conts = p[9]
        elif p[8] ==';':
            init = p[5]
            update = p[10]
            conts = p[9]
        else:
            init = p[5]
            predicate = p[7]
            conts = p[10]
    elif len(p) == 16:
        body = p[13]
        brks = p[15]
        tl_jumps = p[12]
        if p[6] == ';' and p[8] == ';':
            init = p[5]
            conts = p[9]
        elif p[5] == ';' and p[8] == ';':
            predicate = p[7]
            conts = p[9]
        else:
            update = p[9]
            conts = p[8]
    elif len(p) == 15:
        body = p[12]
        brks = p[14]
        tl_jumps = p[11]
        conts = p[8]

    p[0] = For(init = init, predicate = predicate, update = update, body = body)

    tac.backpatch(continues[-1], conts)
    tac.backpatch(breaks[-1], brks)

    tac.backpatch(predicate.truelist, tl_jumps)
    tac.backpatch(predicate.falselist, brks)

    continues.pop()
    breaks.pop()

def p_ForStatementNoShortIf(p):
    '''
    ForStatementNoShortIf : FOR prep_fw_stack LPAREN begin_scope ForInit SEMI for_l1 Expression SEMI for_l1 ForUpdate for_l3 RPAREN for_l1 StatementNoShortIf end_scope for_l2
    | FOR prep_fw_stack LPAREN begin_scope SEMI for_l1 Expression SEMI for_l1 ForUpdate for_l3 RPAREN for_l1 StatementNoShortIf end_scope for_l2
    | FOR prep_fw_stack LPAREN begin_scope ForInit SEMI for_l1 SEMI for_l1 ForUpdate for_l3 RPAREN for_l1 StatementNoShortIf end_scope for_l2
    | FOR prep_fw_stack LPAREN begin_scope ForInit SEMI for_l1 Expression SEMI for_l1 for_l3 RPAREN for_l1 StatementNoShortIf end_scope for_l2
    | FOR prep_fw_stack LPAREN begin_scope ForInit SEMI for_l1 SEMI for_l1 for_l3 RPAREN for_l1 StatementNoShortIf end_scope for_l2
    | FOR prep_fw_stack LPAREN begin_scope SEMI for_l1 Expression SEMI for_l1 for_l3 RPAREN for_l1 StatementNoShortIf end_scope for_l2
    | FOR prep_fw_stack LPAREN begin_scope SEMI for_l1 SEMI for_l1 ForUpdate for_l3 RPAREN for_l1 StatementNoShortIf end_scope for_l2
    | FOR prep_fw_stack LPAREN begin_scope SEMI for_l1 SEMI for_l1 for_l3 RPAREN for_l1 StatementNoShortIf end_scope for_l2
    '''
    init, predicate, update, body, conts, brks, tl_jumps =None, None, None, None, None, None, None
    if len(p) == 18:
        init = p[5]
        predicate = p[8]
        update = p[11]
        body = p[15]
        conts = p[10]
        brks = p[17]
        tl_jumps = p[14]
    elif len(p) == 17:
        body = p[14]
        brks = p[16]
        tl_jumps = p[13]
        if p[5] ==';':
            predicate = p[7]
            update = p[10]
            conts = p[9]
        elif p[8] ==';':
            init = p[5]
            update = p[10]
            conts = p[9]
        else:
            init = p[5]
            predicate = p[7]
            conts = p[10]
    elif len(p) == 16:
        body = p[13]
        brks = p[15]
        tl_jumps = p[12]
        if p[6] == ';' and p[8] == ';':
            init = p[5]
            conts = p[9]
        elif p[5] == ';' and p[8] == ';':
            predicate = p[7]
            conts = p[9]
        else:
            update = p[9]
            conts = p[8]
    elif len(p) == 15:
        body = p[12]
        brks = p[14]
        tl_jumps = p[11]
        conts = p[8]

    p[0] = For(init = init, predicate = predicate, update = update, body = body)

    tac.backpatch(continues[-1], conts)
    tac.backpatch(breaks[-1], brks)

    tac.backpatch(predicate.truelist, tl_jumps)
    tac.backpatch(predicate.falselist, brks)

    continues.pop()
    breaks.pop()

def p_for_l1(p):
    '''
    for_l1 : 
    '''
    label = 'for_' + ST.make_label()
    p[0] = label
    tac.emit('label :', '', '', label)

def p_for_l2(p):
    '''
    for_l2 :
    '''
    label = 'for_' + ST.make_label()
    p[0] = label
    if p[-6] == ';':
        tac.emit('goto', '', '', p[-5])
    else:
        tac.emit('goto','', '', p[-6])
    tac.emit('label :', '', '', label)

def p_for_l3(p):
    '''
    for_l3 :
    '''
    if p[-6] == ';':
        tac.emit('goto','', '', p[-5])
    elif p[-5] == ';':
        tac.emit('goto','', '', p[-4])
    else:
        tac.emit('goto','', '', p[-3])

def p_ForInit(p):
    '''
    ForInit : StatementExpressionList
    | LocalVariableDeclaration
    '''
    p[0]=p[1]

def p_ForUpdate(p):
    '''
    ForUpdate : StatementExpressionList
    '''
    p[0]=p[1]

def p_StatementExpressionList(p):
    '''
    StatementExpressionList : StatementExpression
    | StatementExpressionList COMMA StatementExpression
    '''
    if len(p)==2: p[0]=[p[1]]
    else: p[0]=p[1]+[p[2]]

def p_BreakStatement(p):
    '''
    BreakStatement : BREAK IDENTIFIER SEMI
    | BREAK SEMI
    '''
    if len(p) == 3: 
        breaks[-1].append(len(tac.code))
        tac.emit('goto', '', '', '')
        p[0] = Break()
    else: p[0] = Break(label = p[2])


### BG END

def p_ContinueStatement(p):
    '''
    ContinueStatement : CONTINUE IDENTIFIER SEMI
    | CONTINUE SEMI
    '''
    if len(p) == 3:
        continues[-1].append(len(tac.code))
        tac.emit('goto', '', '', '')
        p[0] = Continue()
    else:
        p[0] = Continue(p[2])

def p_ReturnStatement(p):
    '''
    ReturnStatement : RETURN Expression SEMI
    | RETURN SEMI
    '''
    if len(p) == 3:
        p[0] = Return()
    else:
        p[0] = Return(p[2])
    
def p_Primary(p):
    '''
    Primary : PrimaryNoNewArray
    | ArrayCreationExpression
    '''
    p[0] = p[1]

def p_PrimaryNoNewArray(p):
    '''
    PrimaryNoNewArray : Literal
    | THIS
    | LPAREN Expression RPAREN
    | ClassInstanceCreationExpression
    | FieldAccess
    | MethodInvocation
    | ArrayAccess
    '''
    if len(p)==4:
        p[0] = p[2]
    else :
        p[0] = p[1]

def p_ClassInstanceCreationExpression(p):
    '''
    ClassInstanceCreationExpression : NEW ClassType LPAREN RPAREN
    | NEW ClassType LPAREN ArgumentList RPAREN
    '''
    if len(p) == 5: p[0] = InstanceCreation(type = [2])
    else: p[0] = InstanceCreation(type = p[2], arguments = p[4])

def p_ArgumentList(p):
    '''
    ArgumentList : Expression
    | ArgumentList COMMA Expression
    '''
    if len(p) == 2: p[0] = [p[1]]
    else: p[0] = p[1] + [p[3]]

def p_ArrayCreationExpression(p):
    '''
    ArrayCreationExpression : NEW PrimitiveType DimExprs Dims
    | NEW PrimitiveType DimExprs
    | NEW ClassType DimExprs Dims
    | NEW ClassType DimExprs
    '''
    p[0] = ArrayCreation(p[2], dimensions=p[3])

def p_DimExprs(p):
    '''
    DimExprs : DimExpr
    | DimExprs DimExpr
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_DimExpr(p):
    '''
    DimExpr : LBRACK Expression RBRACK
    '''
    p[0] = p[2]


def p_Dims(p):
    '''
    Dims : LBRACK RBRACK
    | Dims LBRACK RBRACK
    '''
    if len(p) == 3:
        p[0] = 1
    else:
        p[0] = 1 + p[1]

def p_FieldAccess(p):
    '''
    FieldAccess : Primary DOT Name
    | SUPER DOT Name
    '''
    p[0] = FieldAccess(p[3], p[1])

def p_MethodInvocation(p):
    '''
    MethodInvocation : Primary DOT IDENTIFIER LPAREN ArgumentList RPAREN
    | Name LPAREN ArgumentList RPAREN
    | Primary DOT IDENTIFIER LPAREN RPAREN
    | Name LPAREN RPAREN
    '''
    if len(p)==5:
        p[0] = MethodInvocation(p[1], arguments=p[3])
    elif len(p)==7:
        p[0] = MethodInvocation(p[3], target=p[1], arguments=p[5])
    elif len(p)==4:
        p[0] = MethodInvocation(p[1])
    elif len(p)==6:
        p[0] = MethodInvocation(p[3], target=p[1])
    

def p_ArrayAccess(p):
    '''
    ArrayAccess : Name LBRACK Expression RBRACK
    | PrimaryNoNewArray LBRACK Expression RBRACK
    '''
    p[0] = ArrayAccess(p[3], p[1])

def p_PostfixExpression(p):
    '''
    PostfixExpression : Primary
    | Name
    | PostIncrementExpression
    | PostDecrementExpression
    '''
    p[0] = p[1]

def p_PostIncrementExpression(p):
    '''
    PostIncrementExpression : PostfixExpression INC
    '''
    p[0] = Unary('x++', p[1])

def p_PostDecrementExpression(p):
    '''
    PostDecrementExpression : PostfixExpression DEC
    '''
    p[0] = Unary('x--', p[1])

def p_UnaryExpression(p):
    '''
    UnaryExpression : PreIncrementExpression
    | PreDecrementExpression
    | ADD UnaryExpression
    | SUB UnaryExpression
    | UnaryExpressionNotAddSub
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Unary(p[1], p[2])

def p_PreIncrementExpression(p):
    '''
    PreIncrementExpression : INC UnaryExpression
    '''
    p[0] = Unary('++x', p[2])

def p_PreDecrementExpression(p):
    '''
    PreDecrementExpression : DEC UnaryExpression
    '''
    p[0] = Unary('--x', p[2])

def p_UnaryExpressionNotAddSub(p):
    '''
    UnaryExpressionNotAddSub : PostfixExpression
    | BANG UnaryExpression
    | TILDE UnaryExpression
    | CastExpression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Unary(p[1], p[2])

def p_CastExpression(p):
    '''
    CastExpression : LPAREN PrimitiveType Dims RPAREN UnaryExpression
    '''
    p[0] = Cast(Type(p[2], dimensions=p[3]), p[5])

def p_CastExpression2(p):
    '''
    CastExpression :  LPAREN PrimitiveType RPAREN UnaryExpression
    '''
    p[0] = Cast(Type(p[2]), p[4])

def p_CastExpression3(p):
    '''
    CastExpression : LPAREN Expression RPAREN UnaryExpressionNotAddSub
    '''
    p[0] = Cast(Type(p[2]), p[4])
def p_CastExpression4(p):
    '''
    CastExpression : LPAREN Name Dims RPAREN UnaryExpressionNotAddSub
    '''
    p[0] = Cast(Type(p[2], dimensions=p[3]), p[5])

def p_MultiplicativeExpression(p):
    '''
    MultiplicativeExpression : UnaryExpression
    | MultiplicativeExpression MUL UnaryExpression
    | MultiplicativeExpression DIV UnaryExpression
    | MultiplicativeExpression MOD UnaryExpression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Multiplicative(p[2], p[1], p[3])


def p_AdditiveExpression(p):
    '''
    AdditiveExpression : MultiplicativeExpression
    | AdditiveExpression ADD MultiplicativeExpression
    | AdditiveExpression SUB MultiplicativeExpression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Additive(p[2], p[1], p[3])


def p_ShiftExpression(p):
    '''
    ShiftExpression : AdditiveExpression
    | ShiftExpression LSHIFT AdditiveExpression
    | ShiftExpression RSHIFT AdditiveExpression
    | ShiftExpression URSHIFT AdditiveExpression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Shift(p[2], p[1], p[3])


def p_RelationalExpression(p):
    '''
    RelationalExpression : ShiftExpression
    | RelationalExpression LT ShiftExpression
    | RelationalExpression GT ShiftExpression
    | RelationalExpression LE ShiftExpression
    | RelationalExpression GE ShiftExpression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Relational(p[2], p[1], p[3])


def p_EqualityExpression(p):
    '''
    EqualityExpression : RelationalExpression
    | EqualityExpression EQUAL RelationalExpression
    | EqualityExpression NOTEQUAL RelationalExpression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Equality(p[2], p[1], p[3])


def p_AndExpression(p):
    '''
    AndExpression : EqualityExpression
    | AndExpression BITAND EqualityExpression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = And(p[2], p[1], p[3])


def p_ExclusiveOrExpression(p):
    '''
    ExclusiveOrExpression : AndExpression
    | ExclusiveOrExpression CARET AndExpression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Xor(p[2], p[1], p[3])


def p_InclusiveOrExpression(p):
    '''
    InclusiveOrExpression : ExclusiveOrExpression
    | InclusiveOrExpression BITOR ExclusiveOrExpression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Or(p[2], p[1], p[3])

def p_ConditionalAndExpression(p):
    '''
    ConditionalAndExpression : InclusiveOrExpression
    | ConditionalAndExpression AND InclusiveOrExpression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ConditionalAnd(p[2], p[1], p[3])

def p_ConditionalOrExpression(p):
    '''
    ConditionalOrExpression : ConditionalAndExpression
    | ConditionalOrExpression OR ConditionalAndExpression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ConditionalOr(p[2], p[1], p[3])

def p_ConditionalExpression(p):
    '''
    ConditionalExpression : ConditionalOrExpression
    | ConditionalOrExpression QUESTION Expression COLON ConditionalExpression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Conditional(p[1], p[3], p[5])

def p_AssignmentExpression(p):
    '''
    AssignmentExpression : ConditionalExpression
    | Assignment
    '''
    p[0] = p[1]

def p_Assignment(p):
    '''
    Assignment : LeftHandSide AssignmentOperator AssignmentExpression
    '''
    p[0] = Assignment(p[2], p[1], p[3])

def p_LeftHandSide(p):
    '''
    LeftHandSide : Name
    | FieldAccess
    | ArrayAccess
    '''
    p[0] = p[1]

def p_AssignmentOperator(p):
    '''
    AssignmentOperator : ASSIGN
    | ADD_ASSIGN
    | SUB_ASSIGN
    | MUL_ASSIGN   
    | DIV_ASSIGN
    | AND_ASSIGN
    | OR_ASSIGN
    | XOR_ASSIGN
    | MOD_ASSIGN
    | LSHIFT_ASSIGN
    | RSHIFT_ASSIGN
    | URSHIFT_ASSIGN
    '''
    p[0] = p[1]

def p_Expression(p):
    '''
    Expression : AssignmentExpression
    '''
    p[0] = p[1]

def p_ConstantExpression(p):
    '''
    ConstantExpression : Expression
    '''
    p[0] = p[1]

def p_error(p):
    print("Syntax Error in line", p.lineno)

def p_decl_mark(p):
    '''
    decl_mark :
    '''
    var=p[-2]
    if type(p[-2])!=str: var=p[-2].value
    ST.create_new_table(var)
    #print(f"table vreated: {var}")
    # stackbegin.append(var)
    # stackend.append(var)

def p_decl_mark_2(p):
    '''
    decl_mark_2 :
    '''
    ST.create_new_table(p[-1], scope_type="class")
    # stackbegin.append(p[-1])
    # stackend.append(p[-1])

def p_begin_scope(p):
    '''
    begin_scope :
    '''
    l1 = ST.make_label()
    ST.create_new_table(p[-1] + l1)
    # stackbegin.append(p[-1] + l1)
    # stackend.append(p[-1] + l1)

def p_end_scope(p):
    '''
    end_scope :
    '''
    ST.end_scope()
    # stackbegin.pop()
    # stackend.pop()


def main():
    tokens = lexer.tokens
    parser = yacc.yacc()
    inputfile = sys.argv[1]
    file_out = inputfile.split('/')[-1].split('.')[0]
    code = open(inputfile, 'r').read()
    code += "\n"
    parser.parse(code, debug=0)


if __name__ == "__main__":
    main()
