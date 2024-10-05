from ply import lex
import ply.yacc as yacc
import sys


"""
# Grammer

Z -> Sexp

Sexp -> '(' '+' Lista ')'
     | '(' '*' Lista ')'
     | num

Lista -> Lista Sexp
      | Sexp Sexp

"""

literals = ['+', '*', '(', ')']
tokens = ["num"]


def t_num(t):
	r'\d'
	t.value = int(t.value)
	return t

t_ignore = " \n\t"

def t_error(t):
	print("ERROR:", t)

lexer = lex.lex()


def somatorio(lista):
	res = 0
	for e in lista:
		res = res + e
	return res

def produtorio(lista):
	res = 1
	for e in lista:
		res = res * e
	return res

def p_Z(p):
	"Z : Sexp"
	print(p[1])

def p_Sexp_ad(p):
	"Sexp : '(' '+' Lista ')'"
	p[0] = somatorio(p[3])

def p_Sexp_mul(p):
	"Sexp : '(' '*' Lista ')'"
	p[0] = produtorio(p[3])

def p_Sexp_num(p):
	"Sexp : num"
	p[0] = p[1]

def p_Lista_ls(p):
	"Lista : Lista Sexp"
	p[0] = p[1] + [p[2]]

def p_Lista_ss(p):
	"Lista : Sexp Sexp"
	p[0] = [p[1]] + [p[2]]

def p_error(p):
	print("ERROR:", p)
	parser.success = False

parser = yacc.yacc()

for line in sys.stdin:
	parser.success = True
	parser.parse(line)