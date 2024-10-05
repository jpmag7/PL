from ply import lex
import ply.yacc as yacc
import sys


"""
Grammer

Z -> Exp '.'

Exp -> Termo Exp2

Exp2 -> '+' Exp
	 | '-' Exp
	 | Vazio

Termo -> Fator Termo2
	 
Termo2 -> '*' Termo
	   | '/' Termo
	   | Vazio

Fator -> id
	  | num
	  | '(' Exp ')'
"""

literals = ['.', '+', '-', '*', '/', '(', ')']
tokens = ["num", "id"]

t_ignore = " \n\t"

t_id = r"[A-Za-z_]\w*"

def t_newline(t):
	r"\n+"
	t.lexer.lineno += len(t.value)

def t_num(t):
	r'\d'
	t.value = int(t.value)
	return t

def t_error(t):
	print("ERROR:", t)

lexer = lex.lex()




def p_Z(p):
	"Z : Sexp"
	print(p[1])

def p_Exp_ad(p):
	"Exp : Termo Exp2"