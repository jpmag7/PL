import ply.yacc as yacc 
from lexer import tokens, literals 
import sys
import re

def p_Z(p):
	"Z : Init"

def p_Init_cod(p):
	"Init : Cod"

def p_Init_comment(p):
	"Init : COMMENT"

def p_Init_cod_comment(p):
	"Init : Cod COMMENT"

def p_Init_none(p):
	"Init : "

def p_Cod_lex(p):
	"Cod : Lex"
	parser.lex.append(p[1] + "\n")

def p_Cod_yacc(p):
	"Cod : Yacc"
	parser.yacc.append(p[1] + "\n")

def p_Cod_py(p):
	"Cod : Python"
	parser.python.append(p[1])

def p_Lex_start(p):
	"Lex : LEXSTART"
	p[0] = "# LEXER\nimport ply.lex as lex\n"

def p_Lex_literals(p):
	"Lex : '%' LITERALS '=' STRING"
	p[0] = "literals = " + p[4] + "\n"

def p_Lex_ignore(p):
	"Lex : '%' IGNORE '=' STRING"
	p[0] = "t_" + p[2] + " = " + p[4] + "\n"

def p_Lex_tokens(p):
	"Lex : '%' TOKENS '=' LISTA"
	p[0] = "tokens = " + p[4] + "\n"

def p_Lex_states(p):
	"Lex : '%' STATES '=' LISTA"
	p[0] = "states = " + p[4] + "\n"

def p_Lex_reserved(p):
	"Lex : '%' RESERVED '=' DICIONARY"
	p[0] = "reserved = " + p[4] + "\n"
 
def p_Lex_re(p):
	"Lex : STRING RETURN '(' ID ',' CODE ')'"
	p[0] = "def t_" + p[4] + "(t):\n\tr" + p[1] + get_code(p[6], "\n\t") + "return t\n"

def p_Lex_error(p):
	"Lex : LEXERROR '(' STRING ',' CODE ')'"
	if p[3] != "\"\"": prt = "\n\tprint(" + p[3] + ")"
	else: prt = ""
	p[0] = "def t_" + p[1] + "(t):" + prt + get_code(p[5], "\n\t")

def p_Yacc_start(p):
	"Yacc : YACCSTART"
	p[0] = "# YACC\nimport ply.yacc as yacc\n"

def p_Yacc_precedence(p):
	"Yacc : '%' PRECEDENCE '=' LISTA"
	p[0] = "precedence = " + p[4] + "\n"

def p_Yacc_production(p):
	"Yacc : ID PRODUCTION CODE"
	p[0] = "def p_" + p[1] + "_" + str(parser.count) + "(t):\n\t\" " + p[1] + " " + re.sub(r' +', ' ', p[2]) + "\"" + get_code(p[3],"\n\t")
	parser.count = parser.count + 1

def p_Yacc_variable(p):
	"Yacc : VARIABLE"
	p[0] = p[1] + "\n"

def p_Yacc_error(p):
	"Yacc : YACCERROR '(' STRING ',' CODE ')'"
	if p[3] != "\"\"": prt = "\n\tprint(" + p[3] + ")"
	else: prt = ""
	p[0] = "def p_error(t):" + prt + get_code(p[5], "\n\t")

def p_Python_start(p):
	"Python : PYTHON"
	p[0] = "# PYTHON\n"

def p_Python_line(p):
	"Python : LINE"
	p[0] = p[1]

def p_error(p):
	print("ERROR:", p)

def get_code(l, join):
	if len(l) == 0: 
		return join
	code = join
	for v in l:
		if v != '':
			code = code + v + join
	return code


parser = yacc.yacc()

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