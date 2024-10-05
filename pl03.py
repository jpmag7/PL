import sys
import re
import string

def word_counter():
	p = re.compile(r"\b\w+\b")
	file = open("input.txt", "r")
	print(p.findall(file.read()))

def emails():
	p = re.compile(r"(?P<user>^(?:\w+|\W+)+)@(?P<mail>(?:\w+|\W+)+)\.pt$")
	for line in sys.stdin:
		for (user, mail) in p.findall(line):
			invalidChars = set(string.punctuation.replace("_", ""))
			if user[0] in invalidChars or user[-1:] in invalidChars:
				print("Inválido")
				break
			else:
				sair = False
				for c in range(len(user)-1):
					if user[c] in invalidChars and user[c+1] in invalidChars:
						print("Inválido")
						sair = True
						break
				if sair:
					break
			if mail[0] in invalidChars or mail[-1:] in invalidChars:
				print("Inválido")
				break
			else:
				sair = False
				for c in range(len(mail)-1):
					if mail[c] in invalidChars and mail[c+1] in invalidChars:
						print("Inválido")
						sair = True
						break
				if sair:
					break
			print("Válido")




def scrapper():
	p = re.compile(r"(?i)(?:HREF\s*=\s*\"((\w|\W)+)\")")
	for line in sys.stdin:
		for e in p.finditer(line):
			print(e.group(1))

def math():
	p = re.compile(r"(\d+)|([+\-*/])")
	for line in sys.stdin:
		tokens = p.finditer(line)
		for n in tokens:
			if n.group(1):
				print("Int: ", n.group(1))
			else:
				print("Op: ", n.group(2))

math()