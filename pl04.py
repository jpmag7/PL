import ply.lex as lex
import ply.yacc as yacc
import sys

tokens = ['id', 'num', 'DUMP']
literals = ['+', '-', '*', '/', '(', ')', '=', '!', '?']

t_id  = r'[_a-zA-Z]\w*'
t_DUMP = r'!!'

def t_num(t):
	r'\d'
	t.value = int(t.value)
	return t

t_ignore = " \n\t"

def p_error(p):
	print("Erro sintático:", p)
	parser.success = False

def p_Comandos_Lista(p):
	"Comando : id '=' Exp"

def p_Comandos_Simples(p):
	"Comandos : Comando"

def p_Comando_Atrib(p):
	"Comando : id '=' Exp"
	p.parser.registos[p[1]] = p[3]

def p_Comando_Escrita(p):
	"Comando : '!' Exp"
	print(p[2])

def p_Comando_Leitura(p):
	"Comando : '?' id"
	valor = input("Intruduza um valor inteiro: ")
	p.parser.registos[p[2]] = int(valor)

def p_Comando_dump(p):
	"Comando : DUMP"
	print(p.parser.registos)

def p_Exp_ad(p):
	"Exp : Exp '+' Termo"
	p[0] = p[1] + p[3]

def p_Exp_sub(p):
	"Exp : Exp '-' Termo"
	p[0] = p[1] - p[3]

def p_Exp_mul(p):
	"Termo : Termo '*' Fator"
	p[0] = p[1] * p[3]

def p_Exp_div(p):
	"Termo : Termo '/' Fator"
	if p[3] != 0:
		p[0] = p[1] / p[3]
	else:
		print("Erro: Divisão por 0...")

def p_Termo_fator(p):
	"Termo : Fator"
	p[0] = p[1]

def p_Termo_grupo(p):
	


parser = yacc.yacc()

parser.registos = {}

for line in sys.stdin:
	parser.success = True
	parser.parse(line)