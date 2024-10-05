import ply.lex as lex
import re

literals = ['%', '=', '[', ']', '(', ')', ':', '{', '}', ',', '.']

tokens = ["LEXSTART", "YACCSTART", "LITERALS", "IGNORE", "TOKENS", "YACCERROR", "DICIONARY",
          "STRING", "LISTA", "RETURN", "LEXERROR", "PRECEDENCE", "COMMENT", "RESERVED",
          "VARIABLE", "PRODUCTION", "LINE", "ID", "CODE", "PYTHON", "STATES"]

states = [
    ("lex", "inclusive"),
    ("yacc", "inclusive"),
    ("python", "inclusive")
]


def t_COMMENT(t):
    r'\#.*'
    return t

def t_LEXSTART(t):
    r'(?i)%%\s*LEX\n?'
    t.lexer.begin("lex")
    return t

def t_YACCSTART(t):
    r'(?i)%%\s*YACC\n?'
    t.lexer.begin("yacc")
    return t

def t_PYTHON(t):
    r'(?i)%%\s*PYTHON\n?'
    t.lexer.begin("python")
    return t

def t_lex_RETURN(t):
    r'return'
    return t

def t_yacc_PRECEDENCE(t):
    r'precedence'
    return t

def t_lex_LEXERROR(t):
    r"(\w+_)?error"
    return t

def t_yacc_YACCERROR(t):
    r"error"
    return t

def t_lex_LITERALS(t):
    r'literals'
    return t

def t_lex_RESERVED(t):
    r'reserved'
    return t

def t_lex_IGNORE(t):
    r'(\w+_)?ignore'
    return t

def t_lex_TOKENS(t):
    r'tokens'
    return t

def t_lex_STATES(t):
    r'states'
    return t

def t_STRING(t):
    r'((f|r)?\"([^\\\"]*(\\\"|\\)?)+\")|(\'([^\\\']*(\\\'|\\)?)+\')'
    return t

def t_CODE(t):
    r'<.*>'
    t.value = re.search(r"<\s*(.*)>", t.value).group(1)
    t.value = m_split(t.value, '|')
    return t

def t_LISTA(t):
    r'\[.*\](\s*\+\s*list\(reserved\.values\(\)\))?'
    return t

def t_DICIONARY(t):
    r'{.*}'
    return t

def t_yacc_PRODUCTION(t):
    r'\s*:([^<\'\#]*(\'.\')?)+'
    return t

def t_ID(t):
    r'\w+'
    return t

def t_yacc_VARIABLE(t):
    r'\w+\s*=\s*[^\n\#]*'
    return t

def t_python_LINE(t):
    r'(.|\s|\t|\n)+'

    if re.match(r"\n", t.value):
        return None
    elif re.match(r"(?i)%%\s*LEX\n?", t.value):
        t.lexer.begin("lex")
        t.type = "LEXSTART"
    elif re.match(r"(?i)%%\s*YACC\n?", t.value):
        t.lexer.begin("yacc")
        t.type = "YACCSTART"
    elif not re.match(r"\t|\s", t.value):
        t.value = "\n" + t.value

    return t

t_ignore = " \t\n"
t_lex_ignore = " \t\n"
t_yacc_ignore = " \t\n"
t_python_ignore = ""

def t_error(t):
    print('Caracter ilegal: ', t.value[0])
    t.lexer.skip(1)

def t_lex_error(t):
    print('Caracter ilegal: ', t.value[0])
    t.lexer.skip(1)

def t_yacc_error(t):
    print('Caracter ilegal: ', t.value[0])
    t.lexer.skip(1)

def t_python_error(t):
    print('Caracter ilegal: ', t.value[0])
    t.lexer.skip(1)

def m_split(string, sep):
    on_string = False
    aspa = None
    for i, c in enumerate(string):
        if on_string:
            if c == sep:
                string = string[:i] + '«' + string[i+1:]
            if c == '\"' and aspa == '\"':
                on_string = False
                aspa = None
            elif c == '\'' and aspa == '\'':
                on_string = False
                aspa = None
        else:
            if c == '\"':
                on_string = True
                aspa = '\"'
            elif c == '\'':
                on_string = True
                aspa = '\''
    lista = string.split(sep)
    for i, elem in enumerate(lista):
        lista[i] = elem.replace('«', sep)
    return lista

lexer = lex.lex()