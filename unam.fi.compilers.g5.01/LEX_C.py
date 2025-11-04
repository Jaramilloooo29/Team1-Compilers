# Team 1 - Subject: Compilers
# Members:
# 1. Cano Nieto Carlos Arturo
# 2. Cortes Bolaños Luis Angel
# 3. Martinez Garcia Luis Angel
# 4. Rodriguez Jaramillo Alejandro
# 5. Urbano Meza Joseph Gael

import ply.lex as lex

erroresLEX = []

# Tokens
tokens = (
    'INT', 'FLOAT', 'CHAR','DOUBLE', 'LONG', 'SHORT',   # Tipos de datos
    'RETURN','IF', 'ELSE',  # KEYWORDS
    'ID', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'GT', 'LT', 'EQUALS', 'IGUALS',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'SEMICOLON',
    'PRINTF', 'STRING'
)

# KEYWORDS
KEYWORDS = {}

# Tipo
def t_tipo(t):
    r'int|float|char|double|long|short'
    t.type = t.value.upper()  # Convertir a mayúsculas para tokens
    return t

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'=='
t_IGUALS  = r'='
t_GT      = r'>'
t_LT      = r'<'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_SEMICOLON = r';'

t_ignore = ' \t'

def t_INT(t):
    r'int|float|char'
    return t

def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_PRINTF(t):
    r'printf'
    return t

def t_RETURN(t):
    r'return'
    return t

def t_STRING(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]  # Quita comillas
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_HEADER(t):
    r'\#include\s*(<[^>]+>|"[^"]+")'
    pass

def t_error(t):
    erroresLEX.append(f"Carácter ilegal '{t.value[0]}' en posición {t.lexpos}")
    t.lexer.skip(1)

lexer = lex.lex()

def analyze_code(code):
    """Analiza código y retorna tokens para el parser"""
    lexer.input(code)
    tokens_list = []
    
    for tok in lexer:
        tokens_list.append({
            'type': tok.type,
            'value': tok.value,
            'lineno': tok.lineno,
            'lexpos': tok.lexpos
        })
    
    return tokens_list

def get_lexical_errors():
    """Retorna errores léxicos para reporte"""
    return erroresLEX.copy()