import sys
import ply.lex as lex
import ply.yacc as yacc
from pytest import Instance
import lexer
from model import *

def p_Goal(p):
    '''Goal : CompilationUnit'''
    p[0] = p[1]

def p_Literal(p):
    ''' Literal : DECIMAL_LITERAL 
    | HEX_LITERAL 
    | BINARY_LITERAL 
    | FLOAT_LITERAL 
    | BOOL_LITERAL 
    | CHAR_LITERAL 
    | STRING_LITERAL 
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
    if len(p)==4:
        p[0] = CompilationUnit(package_declaration=p[1], import_declarations=p[2], type_declarations=p[3])
    elif len(p)==3:
        p[0] = CompilationUnit(package_declaration=p[1], import_declarations=p[2])
    else :
        p[0] = CompilationUnit(package_declaration=p[1])

def p_CompilationUnit2(p):
    '''
    CompilationUnit : PackageDeclaration TypeDeclarations
    | ImportDeclarations
    '''
    # TODO: Can be empty?
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
    PackageDeclaration : PACKAGE Name SEMI
    '''
    p[0] = PackageDeclaration(p[2])

def p_ImportDeclaration(p):
    '''
    ImportDeclaration : SingleTypeImportDeclaration
    | TypeImportOnDemandDeclaration
    '''
    p[0] = p[1]

def p_SingleTypeImportDeclaration(p):
    '''
    SingleTypeImportDeclaration : IMPORT Name SEMI
    '''
    p[0] = ImportDeclaration(p[2])

def p_TypeImportOnDemandDeclaration(p):
    '''
    TypeImportOnDemandDeclaration : IMPORT Name DOT MUL SEMI
    '''
    p[0] = ImportDeclaration(p[2], on_demand=True)

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
    ClassDeclaration : Modifiers CLASS IDENTIFIER  ClassBody
    | CLASS IDENTIFIER  ClassBody
    '''
    if len(p) == 5: p[0] = ClassDeclaration(name = p[3], body = p[4], modifiers = p[1])
    else: p[0] = ClassDeclaration(name = p[2], body = p[3])

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
    p[0] = MethodDeclaration(p[1]['name'], return_type=p[1]['type'], modifiers=p[1]['modifiers'], body=p[2])

    # TODO
    # p[0] = MethodDeclaration(p[1]['name'], parameters=p[1]['parameters'],
    #                                  extended_dims=p[1]['extended_dims'], type_parameters=p[1]['type_parameters'],
    #                                  return_type=p[1]['type'], modifiers=p[1]['modifiers'], body=p[2])

def p_MethodHeader(p):
    '''
    MethodHeader : Modifiers Type MethodDeclarator
    | Type MethodDeclarator
    '''
    if len(p)==3:
        p[0] = {'modifiers': p[1], 'type': p[2], 'name': p[3]}
    else:
        p[0] = {'type': p[2], 'name': p[2], 'modifiers':[]}


def p_MethodHeader2(p):
    '''
    MethodHeader : Modifiers VOID MethodDeclarator
    | VOID MethodDeclarator
    '''
    if len(p)==3:
        p[0] = {'modifiers': p[1], 'name': p[3], 'type':'void'}
    else:
        p[0] = {'name': p[2], 'type':'void', 'modifiers':[]}



def p_MethodDeclarator(p):
    '''
    MethodDeclarator : IDENTIFIER LPAREN RPAREN
    | IDENTIFIER LPAREN FormalParameterList RPAREN
    '''
    p[0]={}
    if len(p)==4:
        p[0]['name']=p[1]
    else :
        p[0]['name']=p[1]
        p[0]['parameters']=p[3]

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
    StaticInitializer : STATIC Block
    '''
    p[0] = ClassInitializer(p[2], static = True)


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
    p[0]=ConstructorDeclaration(name=declarator['simple_name'], block=body['block_statements'], modifiers=modifiers, type_parameters=None, parameters=declarator['formal_parameter_list'], throws=None)

def p_ConstructorDeclarator(p):
    '''
    ConstructorDeclarator : SimpleName LPAREN FormalParameterList RPAREN
    | SimpleName LPAREN RPAREN
    '''
    param_list=[]       # empty list of params
    if len(p)==5:
        param_list=p[3]
    p[0]={
        'simple_name': p[1],
        'formal_parameter_list': param_list
    }

def p_ConstructorBody(p):
    '''
    ConstructorBody :
    | LBRACE BlockStatements RBRACE
    | LBRACE RBRACE
    '''
    constructor_invocation, block_statements=None, None
    if len(p)==4:
        # if p[2].has_key('argument_list'): constructor_invocation=p[2]
        # else: block_statements=p[2]
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
    IfThenStatement : IF LPAREN Expression RPAREN Statement
    '''
    p[0]=IfThenElse(predicate=p[3], if_true=p[5])

def p_IfThenElseStatement(p):
    '''
    IfThenElseStatement : IF LPAREN Expression RPAREN StatementNoShortIf ELSE Statement
    '''
    p[0]=IfThenElse(predicate=p[3], if_true=p[5], if_false=p[7])

def p_IfThenElseStatementNoShortIf(p):
    '''
    IfThenElseStatementNoShortIf : IF LPAREN Expression RPAREN StatementNoShortIf ELSE StatementNoShortIf
    '''
    p[0]=IfThenElse(predicate=p[3], if_true=p[5], if_false=p[7])

def p_SwitchStatement(p):
    '''
    SwitchStatement : SWITCH LPAREN Expression RPAREN SwitchBlock
    '''
    p[0]=Switch(expression=p[3], switch_cases=p[5])

def p_SwitchBlock(p):
    '''
    SwitchBlock : LBRACE RBRACE
    | LBRACE SwitchBlockStatementGroups SwitchLabels RBRACE
    | LBRACE SwitchBlockStatementGroups RBRACE
    '''
    if len(p)==3: p[0]=[]
    elif len(p)==4: p[0]=p[2]
    else: p[0]=p[2]+[SwitchCase(p[3])]

def p_SwitchBlock2(p):
    '''
    SwitchBlock : LBRACE SwitchLabels RBRACE
    '''
    p[0]=[SwitchCase(p[2])]


def p_SwitchBlockStatementGroups(p):
    '''
    SwitchBlockStatementGroups : SwitchBlockStatementGroup
    | SwitchBlockStatementGroups SwitchBlockStatementGroup
    '''
    if len(p)==2: p[0]=[p[1]]
    else: p[0]=p[1]+[p[2]]

def p_SwitchBlockStatementGroup(p):
    '''
    SwitchBlockStatementGroup : SwitchLabels BlockStatements
    '''
    p[0]=SwitchCase(cases=p[1], body=p[2])

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
    WhileStatement : WHILE LPAREN Expression RPAREN Statement
    '''
    p[0]=While(predicate=p[3], body=p[5])

def p_WhileStatementNoShortIf(p):
    '''
    WhileStatementNoShortIf : WHILE LPAREN Expression RPAREN StatementNoShortIf
    '''
    p[0]=While(predicate=p[3], body=p[5])

def p_DoStatement(p):
    '''
    DoStatement : DO Statement WHILE LPAREN Expression RPAREN SEMI
    '''
    p[0]=DoWhile(predicate=p[5], body=p[2])

def p_ForStatement(p):
    '''
    ForStatement : FOR LPAREN ForInit SEMI Expression SEMI ForUpdate RPAREN Statement
    | FOR LPAREN SEMI Expression SEMI ForUpdate RPAREN Statement
    | FOR LPAREN ForInit SEMI SEMI ForUpdate RPAREN Statement
    | FOR LPAREN ForInit SEMI Expression SEMI RPAREN Statement
    | FOR LPAREN ForInit SEMI SEMI RPAREN Statement
    | FOR LPAREN SEMI Expression SEMI RPAREN Statement
    | FOR LPAREN SEMI SEMI ForUpdate RPAREN Statement
    | FOR LPAREN SEMI SEMI RPAREN Statement
    '''
    init, predicate, update, body=None, None, None, p[-1]
    if len(p)==10:
        init=p[3]
        predicate=p[5]
        update=p[7]
    elif len(p)==9:
        # TODO: Check if p[i]==';' or SEMI
        if p[3]==';':
            predicate=p[4]
            update=p[6]
        elif p[5]==';':
            init=p[3]
            update=p[6]
        else:
            init=p[3]
            predicate=p[5]
    elif len(p)==8:
        if p[4]==';' and p[5]==';':
            init=p[3]
        elif p[3]==';' and p[5]==';':
            predicate=p[4]
        else:
            update=p[5]
    p[0]=For(init=init, predicate=predicate, update=update, body=body)

def p_ForStatementNoShortIf(p):
    '''
    ForStatementNoShortIf : FOR LPAREN ForInit SEMI Expression SEMI ForUpdate RPAREN StatementNoShortIf
    | FOR LPAREN SEMI Expression SEMI ForUpdate RPAREN StatementNoShortIf
    | FOR LPAREN ForInit SEMI SEMI ForUpdate RPAREN StatementNoShortIf
    | FOR LPAREN ForInit SEMI Expression SEMI RPAREN StatementNoShortIf
    | FOR LPAREN ForInit SEMI SEMI RPAREN StatementNoShortIf
    | FOR LPAREN SEMI Expression SEMI RPAREN StatementNoShortIf
    | FOR LPAREN SEMI SEMI ForUpdate RPAREN StatementNoShortIf
    | FOR LPAREN SEMI SEMI RPAREN StatementNoShortIf
    '''
    init, predicate, update, body=None, None, None, p[-1]
    if len(p)==10:
        init=p[3]
        predicate=p[5]
        update=p[7]
    elif len(p)==9:
        # TODO: Check if p[i]==';' or SEMI
        if p[3]==';':
            predicate=p[4]
            update=p[6]
        elif p[5]==';':
            init=p[3]
            update=p[6]
        else:
            init=p[3]
            predicate=p[5]
    elif len(p)==8:
        if p[4]==';' and p[5]==';':
            init=p[3]
        elif p[3]==';' and p[5]==';':
            predicate=p[4]
        else:
            update=p[5]
    p[0]=For(init=init, predicate=predicate, update=update, body=body)

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
    if len(p)==4: p[0]=Break(label=p[2])
    else: p[0]=Break()


### BG END

def p_ContinueStatement(p):
    '''
    ContinueStatement : CONTINUE IDENTIFIER SEMI
    | CONTINUE SEMI
    '''
    if len(p) == 3:
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
    FieldAccess : Primary DOT IDENTIFIER
    | SUPER DOT IDENTIFIER
    '''
    p[0] = FieldAccess(p[3], p[1])

def p_MethodInvocation(p):
    '''
    MethodInvocation : Name LPAREN ArgumentList RPAREN
    | Name LPAREN RPAREN
    | Primary DOT IDENTIFIER LPAREN ArgumentList RPAREN
    | Primary DOT IDENTIFIER LPAREN RPAREN
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