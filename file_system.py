from ply import lex
import ply.yacc as yacc
import sys
import os

"""
# Grammer

Z -> Dird

Dir -> '(' nome Conteudo ')'
	| Ficheiro

Conteudo -> Conteudo Dir
	  	 | Vazio

Ficheiro -> '[' nome path ']'

"""

literals = ['[', ']', '(', ')']
tokens = ["text"]

t_text = r'\"[^"]+'

t_ignore = " \n\t"

def t_error(t):
	print("ERROR:", t)

lexer = lex.lex()

def p_Z(p):
	"Z : Dir"
	print(p[1])

def p_Dir_Pasta(p):
	"Dir : '(' text Conteudo ')'"
	p[0] = [f"mkdir {p[2]}", f"cd  {p[2]}"] + p[3] + ["cd ../"]

def p_Dir_FIcheiro(p):
	"Dir : Ficheiro"
	p[0] = [p[1]]

def p_Conteudo_cd(p):
	"Conteudo : Conteudo Dir"
	p[0] = p[1] + p[2]

def p_Conteudo_vazio(p):
	"Conteudo : "
	p[0] = []

def p_Ficheiro(p):
	"Ficheiro : '[' text text ']'"
	p[0] = f"cp {p[3]} {p[2]}"

def p_error(p):
	print("ERROR:", p)
	parser.success = False

parser = yacc.yacc()

# Input:
""" 
("pl2022" 
	("aulasTeoricas")
	("aulasPraticas")
	("avaliacao" 
		("teste" ["skeleton.tex" "~/template/skeleton.tex"])
		("recurso")
		("especial"))
	("web" ["index.html" "~/templates/index.html"] 
		("imagens" ["prof.jpg" "~/templates/imagens/prof.jpg"] ["um.jpg" "~/templates/imagens/um.jpg"])))
"""
for line in sys.stdin:
	parser.success = True
	parser.parse(line)