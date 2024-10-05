# LEXER
import ply.lex as lex

literals = "%=[]():{},."

tokens = ["LEXSTART", "DICIONARY", "RESERVED", "YACCSTART", "LITERALS", "IGNORE", "TOKENS", "YACCERROR", "STRING", "LISTA", "RETURN", "LEXERROR", "PRECEDENCE", "COMMENT", "VARIABLE", "PRODUCTION", "LINE", "ID", "CODE", "PYTHON", "STATES"]

states = [("lex", "inclusive"),("yacc", "inclusive"),("python", "inclusive")]

t_ignore = " \t\n"

t_lex_ignore = " \t\n"

t_yacc_ignore = " \t\n"

t_python_ignore = ""

def t_COMMENT(t):
	r"\#.*"
	return t

def t_LEXSTART(t):
	r"(?i)%%\s*LEX\n?"
	t.lexer.begin("lex")
	return t

def t_YACCSTART(t):
	r"(?i)%%\s*YACC\n?"
	t.lexer.begin("yacc")
	return t

def t_PYTHON(t):
	r"(?i)%%\s*PYTHON\n?"
	t.lexer.begin("python")
	return t

def t_lex_RETURN(t):
	r"return"
	return t

def t_yacc_PRECEDENCE(t):
	r"precedence"
	return t

def t_lex_LEXERROR(t):
	r"(\w+_)?error"
	return t

def t_yacc_YACCERROR(t):
	r"error"
	return t

def t_lex_LITERALS(t):
	r"literals"
	return t

def t_lex_RESERVED(t):
	r"reserved"
	return t

def t_lex_IGNORE(t):
	r"(\w+_)?ignore"
	return t

def t_lex_TOKENS(t):
	r"tokens"
	return t

def t_lex_STATES(t):
	r"states"
	return t

def t_STRING(t):
	r"((f|r)?\"([^\\\"]*(\\\"|\\)?)+\")|(\"([^\\\"]*(\\\"|\\)?)+\")"
	return t

def t_CODE(t):
	r"<.*>"
	t.value = re.search(r"<\s*(.*)>", t.value).group(1)
	t.value = m_split(t.value, '|')
	return t

def t_LISTA(t):
	r"\[.*\]"
	return t

def t_DICIONARY(t):
	r"{.*}"
	return t

def t_yacc_PRODUCTION(t):
	r"\s*:([^<\"\#]*(\".\")?)+"
	return t

def t_ID(t):
	r"\w+"
	return t

def t_yacc_VARIABLE(t):
	r"\w+\s*=\s*[^\n\#]*"
	return t

def t_python_LINE(t):
	r"(.|\s|\t|\n)+"
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

def t_error(t):
	print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")
	t.lexer.skip(1)
	
def t_lex_error(t):
	print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")
	t.lexer.skip(1)
	
def t_yacc_error(t):
	print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")
	t.lexer.skip(1)
	
def t_python_error(t):
	print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")
	t.lexer.skip(1)
	
lexer = lex.lex()

# YACC
import ply.yacc as yacc

def p_Z_0(t):
	" Z : Init "
	
def p_Init_1(t):
	" Init : Cod "
	
def p_Init_2(t):
	" Init : COMMENT "
	
def p_Init_3(t):
	" Init : Cod COMMENT "
	
def p_Init_4(t):
	" Init : "
	
def p_Cod_5(t):
	" Cod : Lex "
	parser.lex.append(t[1] + "\n")
	
def p_Cod_6(t):
	" Cod : Yacc "
	parser.yacc.append(t[1] + "\n")
	
def p_Cod_7(t):
	" Cod : Python "
	parser.python.append(t[1])
	
def p_Lex_8(t):
	" Lex : LEXSTART "
	t[0] = "# LEXER\nimport ply.lex as lex\n"
	
def p_Lex_9(t):
	" Lex : '%' LITERALS '=' STRING "
	t[0] = "literals = " + t[4] + "\n"
	
def p_Lex_10(t):
	" Lex : '%' IGNORE '=' STRING "
	t[0] = "t_" + t[2] + " = " + t[4] + "\n"
	
def p_Lex_11(t):
	" Lex : '%' TOKENS '=' LISTA "
	t[0] = "tokens = " + t[4] + "\n"
	
def p_Lex_12(t):
	" Lex : '%' STATES '=' LISTA "
	t[0] = "states = " + t[4] + "\n"
	
def p_Lex_13(t):
	" Lex : '%' RESERVED '=' DICIONARY "
	t[0] = "reserved = " + t[4] + "\n"
	
def p_Lex_14(t):
	" Lex : STRING RETURN '(' ID ',' CODE ')' "
	t[0] = "def t_" + t[4] + "(t):\n\tr" + t[1] + get_code(t[6], "\n\t") + "return t\n"
	
def p_Lex_15(t):
	" Lex : LEXERROR '(' STRING ',' CODE ')' "
	if t[3] != "\"\"": prt = "\n\tprint(" + t[3] + ")"
	else: prt = ""
	t[0] = "def t_" + t[1] + "(t):" + prt + get_code(t[5], "\n\t")
	
def p_Yacc_16(t):
	" Yacc : YACCSTART "
	t[0] = "# YACC\nimport ply.yacc as yacc\n"
	
def p_Yacc_17(t):
	" Yacc : '%' PRECEDENCE '=' LISTA "
	t[0] = "precedence = " + t[4] + "\n"
	
def p_Yacc_18(t):
	" Yacc : ID PRODUCTION CODE "
	t[0] = "def p_" + t[1] + "_" + str(parser.count) + "(t):\n\t\" " + t[1] + " " + re.sub(r' +', ' ', t[2]) + "\"" + get_code(t[3],"\n\t")
	parser.count = parser.count + 1
	
def p_Yacc_19(t):
	" Yacc : VARIABLE "
	t[0] = t[1] + "\n"
	
def p_Yacc_20(t):
	" Yacc : YACCERROR '(' STRING ',' CODE ')' "
	if t[3] != "\"\"": prt = "\n\tprint(" + t[3] + ")"
	else: prt = ""
	t[0] = "def p_error(t):" + prt + get_code(t[5], "\n\t")
	
def p_Python_21(t):
	" Python : PYTHON "
	t[0] = "# PYTHON\n"
	
def p_Python_22(t):
	" Python : LINE "
	t[0] = t[1]
	
def p_error(t):
	print(t)
	
parser = yacc.yacc()

# PYTHON

import sys

import re

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

def get_code(l, join):
	if len(l) == 0: 
		return join
	code = join
	for v in l:
		if v != '':
			code = code + v + join
	return code

def run(inp, out):
	parser.count  = 0
	parser.lex    = []
	parser.yacc   = []
	parser.python = []
	for line in inp:
		parser.parse(line)
	for line in parser.lex:
		out.write(line)
	out.write("lexer = lex.lex()\n\n")
	for line in parser.yacc:
		out.write(line)
	out.write("parser = yacc.yacc()\n\n")
	for line in parser.python:
		out.write(line)

def main():
	if len(sys.argv) == 1:
		run(sys.stdin, sys.stdout)
	elif len(sys.argv) == 2:
		out = open(sys.argv[1], "w", encoding="utf-8")
		run(sys.stdin, out)
		out.close()
	else:
		inp = open(sys.argv[1], "r", encoding="utf-8")
		out = open(sys.argv[2], "w", encoding="utf-8")
		run(inp, out)
		inp.close()
		out.close()

main()