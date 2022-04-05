import ply.lex as lex
import sys
#keywords

keywords = {
    'boolean':'BOOLEAN',
    'break':'BREAK',
    'byte':'BYTE',
    'case':'CASE',
    'char':'CHAR',
    'class':'CLASS',
    # 'const': 'CONST',
    'continue':'CONTINUE',
    'default':'DEFAULT',
    'do':'DO',
    'double':'DOUBLE',
    'else':'ELSE',
    'final':'FINAL',
    'float':'FLOAT',
    'null' : 'NULL',
    'for':'FOR',
    'if':'IF',
    'import':'IMPORT',
    'int':'INT',
    'long':'LONG',
    'new':'NEW',
    'package':'PACKAGE',
    'private':'PRIVATE',
    'protected':'PROTECTED',
    'public':'PUBLIC',
    'return':'RETURN',
    'short':'SHORT',
    'static':'STATIC',
    'super':'SUPER',
    'switch':'SWITCH',
    'this':'THIS',
    'void':'VOID',
    'while':'WHILE',

}

#seperator

seperators = [
    'LPAREN','RPAREN','LBRACE','RBRACE','LBRACK','RBRACK','SEMI','COMMA','DOT'
]

#operators

operators = [
    'ASSIGN',      
    'GT',         
    'LT',          
    'BANG',         
    'TILDE',        
    'QUESTION',     
    'COLON',    
    'EQUAL',       
    'LE',       
    'GE',          
    'NOTEQUAL',     
    'AND',    
    'OR',         
    'INC',          
    'DEC',         
    'ADD',          
    'SUB',          
    'MUL',          
    'DIV',          
    'BITAND',       
    'BITOR',        
    'CARET',     
    'MOD',          
    'ADD_ASSIGN',   
    'SUB_ASSIGN',   
    'MUL_ASSIGN',   
    'DIV_ASSIGN',   
    'AND_ASSIGN',   
    'OR_ASSIGN',   
    'XOR_ASSIGN',  
    'MOD_ASSIGN',  
    'LSHIFT_ASSIGN',
    'RSHIFT_ASSIGN',
    'URSHIFT_ASSIGN',
    'LSHIFT',
    'RSHIFT',
    'URSHIFT',
]

#literals

literal = [
    'DECIMAL_LITERAL',
    'HEX_LITERAL',
    'BINARY_LITERAL',
    'FLOAT_LITERAL',
    'BOOL_LITERAL',
    'CHAR_LITERAL',
    'STRING_LITERAL'
]

tokens = seperators + operators + list(keywords.values()) + literal + ['IDENTIFIER']

#regex for seperators

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_SEMI = r';'
t_COMMA = r','
t_DOT = r'\.'

#regex for operators

t_ASSIGN         =   r'='
t_GT             =   r'>'
t_LT             =   r'<'
t_BANG           =   r'!'
t_TILDE          =   r'~'
t_QUESTION       =   r'\?'
t_COLON          =   r':'
t_EQUAL          =   r'=='
t_LE             =   r'<='
t_GE             =   r'>='
t_NOTEQUAL       =   r'!='
t_AND            =   r'&&'
t_OR             =   r'\|\|'
t_INC            =   r'\+\+'
t_DEC            =   r'--'
t_ADD            =   r'\+'
t_SUB            =   r'\-'
t_MUL            =   r'\*'
t_DIV            =   r'/'
t_BITAND         =   r'&'
t_BITOR          =   r'\|'
t_CARET          =   r'\^'
t_MOD            =   r'%'
t_ADD_ASSIGN     =   r'\+='
t_SUB_ASSIGN     =   r'\-='
t_MUL_ASSIGN     =   r'\*='
t_DIV_ASSIGN     =   r'/='
t_AND_ASSIGN     =   r'&='
t_OR_ASSIGN      =   r'\|='
t_XOR_ASSIGN     =   r'\^='
t_MOD_ASSIGN     =   r'%='
t_LSHIFT         =   r'<<'
t_RSHIFT         =   r'>>'
t_URSHIFT        =   r'>>>'
t_LSHIFT_ASSIGN  =   r'<<='
t_RSHIFT_ASSIGN  =   r'>>='
t_URSHIFT_ASSIGN =   r'>>>='

#ignore whitespaces

t_ignore = ' \t'  

# fragments

#regex for literals
# t_FLOAT_LITERAL =   r'\d*\.\d+'
# t_DECIMAL_LITERAL =  r'(0|[1-9](([0-9]([0-9_]*[0-9])?)?|_+([0-9]([0-9_]*[0-9])?)))[lL]?'
# t_FLOAT_LITERAL = fr'({f_DIGITS}\.{f_DIGITS}?|\.{f_DIGITS}){f_EXPONENT_PART}?[fFdD]?|{f_DIGITS}({f_EXPONENT_PART}[fFdD]?|[fFdD])'
# t_HEX_LITERAL =       r'0[xX][0-9a-fA-F]+[lL]?'
# t_BINARY_LITERAL =    r'0[bB][01]+[lL]?'
# t_DECIMAL_LITERAL = fr'([0]|[1-9]\d*)[lL]?'
# t_DECIMAL_LITERAL = r'\d+'
# #t_FLOAT_LITERAL =   r'(([0-9]([0-9_]*[0-9])?)\.([0-9]([0-9_]*[0-9])?)?|\.([0-9]([0-9_]*[0-9])?))([eE][+-]?([0-9]([0-9_]*[0-9])?))?[fFdD]?([0-9]([0-9_]*[0-9])?)(([eE][+-]?([0-9]([0-9_]*[0-9])?))[fFdD]?|[fFdD])'

def t_HEX_LITERAL(t):
    r'0[xX][0-9a-fA-F]+[lL]?'
    return t

def t_BINARY_LITERAL(t):
    r'0[bB][01]+[lL]?'
    return t

def t_FLOAT_LITERAL(t):
    r'\d*\.\d+([eE][+-]?\d+)?[fFdD]?|([0]|[1-9]\d*)[fFdD]|([0]|[1-9]\d*)[eE][+-]?\d+[fFdD]?'
    return t

def t_DECIMAL_LITERAL(t):
    r'([0]|[1-9]\d*)[lL]?'
    return t

def t_BOOL_LITERAL(t):
    r'true|false'
    return t

t_CHAR_LITERAL = r'\'([^\\\n]|(\\.))*?\''
t_STRING_LITERAL = r'\"([^\\\n]|(\\.))*?\"'

def t_IDENTIFIER(t):
    r'[a-zA-Z_$][a-zA-Z_0-9$]*'
    t.type = keywords.get(t.value,'IDENTIFIER')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_LINE_COMMENT(t):
    r'//.*'
    pass

def t_BLOCK_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

def t_error(t):
    print("Illegal character '{}' ({}) in line {}".format(t.value[0], hex(ord(t.value[0])), t.lexer.lineno))
    t.lexer.skip(1)

def find_column(input, token):
     line_start = input.rfind('\n', 0, token.lexpos) + 1
     return (token.lexpos - line_start) + 1

lexer = lex.lex()

def main():
    inp = open(sys.argv[1],"r").read()
    lexer.input(inp)

    output = []
    
    while True:
        token = lexer.token()
        if not token:
            break
        output.append([token.type,token.value,token.lineno,find_column(inp,token)])

    print("| {:20s} | {:20s} | {:5s} | {:5s} |".format("Token", "Lexeme", "Line#", "Col#"))
    print("---------------------------------------------------------------")
    for data in output:
        print("| {:20s} | {:20s} | {:5s} | {:5s} |".format(data[0], data[1], str(data[2]), str(data[3])))
        print("---------------------------------------------------------------")


if __name__ == '__main__':
    main()
