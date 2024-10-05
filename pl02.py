import sys
import re


def input():
	inicio = re.compile(r"^Ola")
	fim = re.compile(r"Ola$")
	toda = re.compile(r"^Ola$")

	f = sys.stdin
	num = int(f.readline())

	for i in range(num):
		l = f.readline()
		if toda.search(l):
			print(0)
		elif inicio.search(l):
			print(1)
		elif fim.search(l):
			print(2)
		else: 
			print(-1)


def usernames():
	p = re.compile(r"^(\.|_)\d+[a-zA-Z]{3,}_?$")

	for line in sys.stdin:
		if p.match(line):
			print("Válido")
		else:
			print("Inválido")


def div3():
	num_at_even = re.compile(r"")
	num_at_odd = re.compile(r"")


def matriculas():
	p = re.compile(r"((\d{2}\.\.\.){3}|(\d{2}:){3}|(\d{2}-){3})\d{2}")
	for line in sys.stdin:
		lista = p.findall(line)
		if p.findall(line):
			print("Válido")
			print(len(lista))
		else:
			print("Inválido")

def gps():
	p = re.compile(r"\((\+|-)?([1-9](\.\d+)?|[1-8](\d{1}(\.\d+)?)?|90(\.0+)?),(\+|-)?([1-9](\.\d+)?|[1-9](\d{1}(\.\d+)?)?|1[0-7]\d{1}(\.\d+)?|180(\.0+)?)\)")
	for line in sys.stdin:
		if p.match(line):
			print("Válido")
		else:
			print("Inválido")

def apanhas():
	int_counter = 0
	state = True
	p = re.compile(r"(\d+|(o|O)(f|F){2}|(o|O)(n|N))")
	for line in sys.stdin:
		lista = p.findall(line)
		for elem in lista:
			try:
				num = int(elem[0])
				if state:
					int_counter = int_counter + num
			except:
				if elem[0].upper() == "OFF":
					state = False
				else:
					state = True
		print("Sum:", int_counter)

apanhas()