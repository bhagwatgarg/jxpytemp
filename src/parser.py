import sys
import ply.lex as lex
import ply.yacc as yacc
import lexer

def p_Goal(p):
    '''Goal : CompilationUnit'''

def p_Literal(p):
    ''' Literal : DECIMAL_LITERAL 
    | HEX_LITERAL 
    | BINARY_LITERAL 
    | FLOAT_LITERAL 
    | BOOL_LITERAL 
    | CHAR_LITERAL 
    | STRING_LITERAL 
    '''

def p_Type(p):
    ''' Type : PrimitiveType
    | ReferenceType
    '''

def p_PrimitiveType(p):
    ''' PrimitiveType : NumericType
    | BOOLEAN
    '''

def p_NumericType(p):
    ''' NumericType : IntegralType
    | FloatingPointType
    '''

def p_IntegralType(p):
    ''' IntegralType : BYTE
    | SHORT
    | INT
    | LONG
    | CHAR
    '''

def p_FloatingPointType(p):
    ''' FloatingPointType : FLOAT
    | DOUBLE
    '''

def p_ReferenceType(p):
    ''' ReferenceType : ArrayType
    | ClassType
    '''

def p_ClassType(p):
    '''
    ClassType : Name
    '''

def p_ArrayType(p):
    ''' ArrayType : PrimitiveType LBRACK RBRACK
    | Name LBRACK RBRACK
    | ArrayType LBRACK RBRACK
    '''

def p_Name(p):
    ''' Name : SimpleName
    | QualifiedName'''

def p_SimpleName(p):
    ''' SimpleName : IDENTIFIER'''

def p_QualifiedName(p):
    ''' QualifiedName : Name DOT IDENTIFIER'''

def p_CompilationUnit(p):
    '''
    CompilationUnit : PackageDeclaration ImportDeclarations TypeDeclarations
    | PackageDeclaration ImportDeclarations
    | PackageDeclaration TypeDeclarations
    | ImportDeclarations TypeDeclarations
    | PackageDeclaration
    | ImportDeclarations
    | TypeDeclarations
    |
    '''

def p_ImportDeclarations(p):
    '''
    ImportDeclarations : ImportDeclaration
    | ImportDeclarations ImportDeclaration
    '''

def p_TypeDeclarations(p):
    '''
    TypeDeclarations : TypeDeclaration
    | TypeDeclarations TypeDeclaration
    '''

def p_PackageDeclaration(p):
    '''
    PackageDeclaration : PACKAGE Name SEMI
    '''

def p_ImportDeclaration(p):
    '''
    ImportDeclaration : SingleTypeImportDeclaration
    | TypeImportOnDemandDeclaration
    '''

def p_SingleTypeImportDeclaration(p):
    '''
    SingleTypeImportDeclaration : IMPORT Name SEMI
    '''

def p_TypeImportOnDemandDeclaration(p):
    '''
    TypeImportOnDemandDeclaration : IMPORT Name DOT MUL SEMI
    '''

def p_TypeDeclaration(p):
    '''
    TypeDeclaration : ClassDeclaration
    | SEMI
    '''

# split this according to titanium http://titanium.cs.berkeley.edu/doc/java-langspec-1.0/19.doc.html
def p_Modifiers(p):
    '''
    Modifiers : Modifier
    | Modifiers Modifier
    '''

def p_Modifier(p):
    '''
    Modifier : STATIC
    | FINAL
    | PRIVATE
    | PROTECTED
    | PUBLIC
    '''

def p_ClassDeclaration(p):
    '''
    ClassDeclaration : Modifiers CLASS IDENTIFIER  ClassBody
    | CLASS IDENTIFIER  ClassBody
    '''

def p_ClassBody(p):
    '''
    ClassBody : LBRACE RBRACE
    | LBRACE ClassBodyDeclarations RBRACE
    '''

def p_ClassBodyDeclarations(p):
    '''
    ClassBodyDeclarations : ClassBodyDeclaration
    | ClassBodyDeclarations ClassBodyDeclaration
    '''

def p_ClassBodyDeclaration(p):
    '''
    ClassBodyDeclaration : ClassMemberDeclaration
    | ConstructorDeclaration
    | StaticInitializer
    '''

def p_ClassMemberDeclaration(p):
    '''
    ClassMemberDeclaration : FieldDeclaration
    | MethodDeclaration
    '''

def p_FieldDeclaration(p):
    '''
    FieldDeclaration : Modifiers Type VariableDeclarators SEMI
    | Type VariableDeclarators SEMI
    '''

def p_VariableDeclarators(p):
    '''
    VariableDeclarators : VariableDeclarator
    | VariableDeclarators COMMA VariableDeclarator
    '''

def p_VariableDeclarator(p):
    '''
    VariableDeclarator : VariableDeclaratorId
    | VariableDeclaratorId ASSIGN VariableInitializer
    '''

def p_VariableDeclaratorId(p):
    '''
    VariableDeclaratorId : IDENTIFIER
    | VariableDeclaratorId LBRACK RBRACK
    '''

def p_VariableInitializer(p):
    '''
    VariableInitializer : Expression
    | ArrayInitializer
    '''

def p_MethodDeclaration(p):
    '''
    MethodDeclaration : MethodHeader MethodBody
    '''

def p_MethodHeader(p):
    '''
    MethodHeader : Modifiers Type MethodDeclarator
    | Type MethodDeclarator
    | Modifiers VOID MethodDeclarator
    | VOID MethodDeclarator
    '''

def p_MethodDeclarator(p):
    '''
    MethodDeclarator : IDENTIFIER LPAREN RPAREN
    | IDENTIFIER LPAREN FormalParameterList RPAREN
    '''

def p_FormalParametersList(p):
    '''
    FormalParameterList : FormalParameter
    | FormalParameterList COMMA FormalParameter
    '''

def p_FormalParameter(p):
    '''
    FormalParameter : Type VariableDeclaratorId
    '''

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

def p_StaticInitializer(p):
    '''
    StaticInitializer : STATIC Block
    '''

def p_ConstructorDeclaration(p):
    '''
    ConstructorDeclaration : Modifiers ConstructorDeclarator ConstructorBody
    | ConstructorDeclarator ConstructorBody
    '''

def p_ConstructorDeclarator(p):
    '''
    ConstructorDeclarator : SimpleName LPAREN FormalParameterList RPAREN
    | SimpleName LPAREN RPAREN
    '''

def p_ConstructorBody(p):
    '''
    ConstructorBody : LBRACE ExplicitConstructorInvocation BlockStatements RBRACE
    | LBRACE ExplicitConstructorInvocation RBRACE
    | LBRACE BlockStatements RBRACE
    | LBRACE RBRACE
    '''

def p_ExplicitConstructorInvocation(p):
    '''
    ExplicitConstructorInvocation : THIS LPAREN ArgumentList RPAREN SEMI
    | THIS LPAREN RPAREN SEMI
    '''

def p_ArrayInitializer(p):
    '''
    ArrayInitializer : LBRACE VariableInitializers RBRACE
    | LBRACE RBRACE
    '''

def p_VariableInitializers(p):
    '''
    VariableInitializers : VariableInitializer
    | VariableInitializers COMMA VariableInitializer
    '''

def p_Block(p):
    '''
    Block : LBRACE RBRACE
    | LBRACE BlockStatements RBRACE
    '''

def p_BlockStatements(p):
    '''
    BlockStatements : BlockStatement
    | BlockStatements BlockStatement
    '''

def p_BlockStatement(p):
    '''
    BlockStatement : LocalVariableDeclarationStatement
    | Statement
    '''

def p_LocalVariableDeclarationStatement(p):
    '''
    LocalVariableDeclarationStatement : LocalVariableDeclaration SEMI
    '''

def p_LocalVariableDeclaration(p):
    '''
    LocalVariableDeclaration : Type VariableDeclarators
    '''

def p_Statement(p):
    '''
    Statement : StatementWithoutTrailingSubstatement
    | LabeledStatement
    | IfThenStatement
    | IfThenElseStatement
    | WhileStatement
    | ForStatement
    '''

def p_StatementNoShortIf(p):
    '''
    StatementNoShortIf : StatementWithoutTrailingSubstatement
    | LabeledStatementNoShortIf
    | IfThenElseStatementNoShortIf
    | WhileStatementNoShortIf
    | ForStatementNoShortIf
    '''

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

def p_EmptyStatement(p):
    '''
    EmptyStatement : SEMI
    '''

def p_LabeledStatement(p):
    '''
    LabeledStatement : IDENTIFIER COLON Statement
    '''

def p_LabeledStatementNoShortIf(p):
    '''
    LabeledStatementNoShortIf : IDENTIFIER COLON StatementNoShortIf
    '''

def p_ExpressionStatement(p):
    '''
    ExpressionStatement : StatementExpression SEMI
    '''

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

def p_IfThenStatement(p):
    '''
    IfThenStatement : IF LPAREN Expression RPAREN Statement
    '''

def p_IfThenElseStatement(p):
    '''
    IfThenElseStatement : IF LPAREN Expression RPAREN StatementNoShortIf ELSE Statement
    '''

def p_IfThenElseStatementNoShortIf(p):
    '''
    IfThenElseStatementNoShortIf : IF LPAREN Expression RPAREN StatementNoShortIf ELSE StatementNoShortIf
    '''

def p_SwitchStatement(p):
    '''
    SwitchStatement : SWITCH LPAREN Expression RPAREN SwitchBlock
    '''

def p_SwitchBlock(p):
    '''
    SwitchBlock : LBRACE RBRACE
    | LBRACE SwitchBlockStatementGroups SwitchLabels RBRACE
    | LBRACE SwitchBlockStatementGroups RBRACE
    | LBRACE SwitchLabels RBRACE
    '''

def p_SwitchBlockStatementGroups(p):
    '''
    SwitchBlockStatementGroups : SwitchBlockStatementGroup
    | SwitchBlockStatementGroups SwitchBlockStatementGroup
    '''

def p_SwitchBlockStatementGroup(p):
    '''
    SwitchBlockStatementGroup : SwitchLabels BlockStatements
    '''

def p_SwitchLabels(p):
    '''
    SwitchLabels : SwitchLabel
    | SwitchLabels SwitchLabel
    '''

def p_SwitchLabel(p):
    '''
    SwitchLabel : CASE ConstantExpression COLON
    | DEFAULT COLON
    '''

def p_WhileStatement(p):
    '''
    WhileStatement : WHILE LPAREN Expression RPAREN Statement
    '''

def p_WhileStatementNoShortIf(p):
    '''
    WhileStatementNoShortIf : WHILE LPAREN Expression RPAREN StatementNoShortIf
    '''

def p_DoStatement(p):
    '''
    DoStatement : DO Statement WHILE LPAREN Expression RPAREN SEMI
    '''

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

def p_ForInit(p):
    '''
    ForInit : StatementExpressionList
    | LocalVariableDeclaration
    '''

def p_ForUpdate(p):
    '''
    ForUpdate : StatementExpressionList
    '''

def p_StatementExpressionList(p):
    '''
    StatementExpressionList : StatementExpression
    | StatementExpressionList COMMA StatementExpression
    '''

def p_BreakStatement(p):
    '''
    BreakStatement : BREAK IDENTIFIER SEMI
    | BREAK SEMI
    '''

def p_ContinueStatement(p):
    '''
    ContinueStatement : CONTINUE IDENTIFIER SEMI
    | CONTINUE SEMI
    '''

def p_ReturnStatement(p):
    '''
    ReturnStatement : RETURN Expression SEMI
    | RETURN SEMI
    '''

def p_Primary(p):
    '''
    Primary : PrimaryNoNewArray
    | ArrayCreationExpression
    '''

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

def p_ClassInstanceCreationExpression(p):
    '''
    ClassInstanceCreationExpression : NEW ClassType LPAREN RPAREN
    | NEW ClassType LPAREN ArgumentList RPAREN
    '''

def p_ArgumentList(p):
    '''
    ArgumentList : Expression
    | ArgumentList COMMA Expression
    '''

def p_ArrayCreationExpression(p):
    '''
    ArrayCreationExpression : NEW PrimitiveType DimExprs Dims
    | NEW PrimitiveType DimExprs
    | NEW ClassType DimExprs Dims
    | NEW ClassType DimExprs
    '''

def p_DimExprs(p):
    '''
    DimExprs : DimExpr
    | DimExprs DimExpr
    '''

def p_DimExpr(p):
    '''
    DimExpr : LBRACK Expression RBRACK
    '''

def p_Dims(p):
    '''
    Dims : LBRACK RBRACK
    | Dims LBRACK RBRACK
    '''

def p_FieldAccess(p):
    '''
    FieldAccess : Primary DOT IDENTIFIER
    | SUPER DOT IDENTIFIER
    '''

def p_MethodInvocation(p):
    '''
    MethodInvocation : Name LPAREN ArgumentList RPAREN
    | Name LPAREN RPAREN
    | Primary DOT IDENTIFIER LPAREN ArgumentList RPAREN
    | Primary DOT IDENTIFIER LPAREN RPAREN
    '''

def p_ArrayAccess(p):
    '''
    ArrayAccess : Name LBRACK Expression RBRACK
    | PrimaryNoNewArray LBRACK Expression RBRACK
    '''

def p_PostfixExpression(p):
    '''
    PostfixExpression : Primary
    | Name
    | PostIncrementExpression
    | PostDecrementExpression
    '''

def p_PostIncrementExpression(p):
    '''
    PostIncrementExpression : PostfixExpression INC
    '''

def p_PostDecrementExpression(p):
    '''
    PostDecrementExpression : PostfixExpression DEC
    '''

def p_UnaryExpression(p):
    '''
    UnaryExpression : PreIncrementExpression
    | PreDecrementExpression
    | ADD UnaryExpression
    | SUB UnaryExpression
    | UnaryExpressionNotAddSub
    '''

def p_PreIncrementExpression(p):
    '''
    PreIncrementExpression : INC UnaryExpression
    '''

def p_PreDecrementExpression(p):
    '''
    PreDecrementExpression : DEC UnaryExpression
    '''

def p_UnaryExpressionNotAddSub(p):
    '''
    UnaryExpressionNotAddSub : PostfixExpression
    | BANG UnaryExpression
    | TILDE UnaryExpression
    | CastExpression
    '''

def p_CastExpression(p):
    '''
    CastExpression : LPAREN PrimitiveType Dims RPAREN UnaryExpression
    | LPAREN PrimitiveType RPAREN UnaryExpression
    | LPAREN Expression RPAREN UnaryExpressionNotAddSub
    | LPAREN Name Dims RPAREN UnaryExpressionNotAddSub
    '''

def p_MultiplicativeExpression(p):
    '''
    MultiplicativeExpression : UnaryExpression
    | MultiplicativeExpression MUL UnaryExpression
    | MultiplicativeExpression DIV UnaryExpression
    | MultiplicativeExpression MOD UnaryExpression
    '''

def p_AdditiveExpression(p):
    '''
    AdditiveExpression : MultiplicativeExpression
    | AdditiveExpression ADD MultiplicativeExpression
    | AdditiveExpression SUB MultiplicativeExpression
    '''

def p_ShiftExpression(p):
    '''
    ShiftExpression : AdditiveExpression
    | ShiftExpression LSHIFT AdditiveExpression
    | ShiftExpression RSHIFT AdditiveExpression
    | ShiftExpression URSHIFT AdditiveExpression
    '''

def p_RelationalExpression(p):
    '''
    RelationalExpression : ShiftExpression
    | RelationalExpression LT ShiftExpression
    | RelationalExpression GT ShiftExpression
    | RelationalExpression LE ShiftExpression
    | RelationalExpression GE ShiftExpression
    '''

def p_EqualityExpression(p):
    '''
    EqualityExpression : RelationalExpression
    | EqualityExpression EQUAL RelationalExpression
    | EqualityExpression NOTEQUAL RelationalExpression
    '''

def p_AndExpression(p):
    '''
    AndExpression : EqualityExpression
    | AndExpression BITAND EqualityExpression
    '''

def p_ExclusiveOrExpression(p):
    '''
    ExclusiveOrExpression : AndExpression
    | ExclusiveOrExpression CARET AndExpression
    '''

def p_InclusiveOrExpression(p):
    '''
    InclusiveOrExpression : ExclusiveOrExpression
    | InclusiveOrExpression BITOR ExclusiveOrExpression
    '''

def p_ConditionalAndExpression(p):
    '''
    ConditionalAndExpression : InclusiveOrExpression
    | ConditionalAndExpression AND InclusiveOrExpression
    '''

def p_ConditionalOrExpression(p):
    '''
    ConditionalOrExpression : ConditionalAndExpression
    | ConditionalOrExpression OR ConditionalAndExpression
    '''

def p_ConditionalExpression(p):
    '''
    ConditionalExpression : ConditionalOrExpression
    | ConditionalOrExpression QUESTION Expression COLON ConditionalExpression
    '''

def p_AssignmentExpression(p):
    '''
    AssignmentExpression : ConditionalExpression
    | Assignment
    '''

def p_Assignment(p):
    '''
    Assignment : LeftHandSide AssignmentOperator AssignmentExpression
    '''

def p_LeftHandSide(p):
    '''
    LeftHandSide : Name
    | FieldAccess
    | ArrayAccess
    '''

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

def p_Expression(p):
    '''
    Expression : AssignmentExpression
    '''

def p_ConstantExpression(p):
    '''
    ConstantExpression : Expression
    '''

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
