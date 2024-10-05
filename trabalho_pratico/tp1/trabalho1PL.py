from os.path import exists
import ply.lex as lex
import sys
import re


tokens = ["WORD", "LIST", "SIZE", "FUNC", "NONE"]

headers = []

t_ignore = '\n \t'

def t_LIST(t):
	r'\s*[^,]+\s*{'                                       # Notas{
	t.value = re.search(r'[^,{\n\t]+', t.value).group()   # Notas
	return t

def t_SIZE(t):
	r'\s*{?\s*\d+(\s*,\s*\d+)?\s*}\s*,?'                  # {3} || {3,4}, || 3}, || 3,4}
	t.value = re.search(r'(\d+)},?', t.value).group(1)    # 3 || 4 || 3 || 4
	return t

def t_FUNC(t):
	r'\s*::[^,:]+\s*,?'                                   # ::sum,
	t.value = re.search(r'[^,:\s\n\t]+', t.value).group() # sum
	return t

def t_WORD(t):
	r'\s*[^,]+\s*,?'                                      # Numero,
	t.value = re.search(r'[^,\n\t]+', t.value).group()    # Numero
	return t

def t_NONE(t):
	r'[^,]*,'    # ,, || , ,
	return t

def t_error(t):
	print("ERRO on lex")
	return t


#Exemplo: ["Numero", "Nome", ["Notas", 5, "sum"],	 "Curso"]
def make_headers(file):
	lexer = lex.lex()
	first_line = file.readline()
	lexer.input(first_line)
	for tok in lexer:
		if tok.type == "LIST": # Notas
			# ["Numero", "Nome"] + ["Notas"] = ["Numero", "Nome", ["Notas"]]
			headers.append([tok.value])
		elif tok.type == "SIZE": # 5
			# ["Numero", "Nome", ["Notas"]][-1] + 5 = ["Numero", "Nome", ["Notas", 5]]
			headers[-1].append(tok.value)
		elif tok.type == "WORD": # Nome
			# ["Numero"] + "Nome" = ["Numero", "Nome"]
			headers.append(tok.value)
		elif tok.type == "FUNC": # sum
			# ["Numero", "Nome", ["Notas", 5]][-1] + "sum" = ["Numero", "Nome", ["Notas", 5, "sum"]]
			headers[-1].append(tok.value)


def soma(l):
	soma = 0
	for elem in l:
		soma = soma + elem
	return soma


"""
header = ["Numero", "Nome", ["Notas", 5, "sum"], "Curso"]
[123,pedro,12,12,12,12,,miei]
{
	Numero : 123
	Nome : pedro
	Notas : [12,12,12,12]
	Sum = 48
	Curso : miei
}
"""
def build_row(results):
	row = {}
	idx = 0
	for header in headers:
		if type(header) == str:
			row[header] = results[idx]
			idx = idx + 1
		elif type(header) == list:
			m_list = []
			for i in range(int(header[1])):
				if results[idx] != "":
					m_list.append(int(results[idx]))
				idx = idx + 1
			row[header[0]] = m_list
			if len(header) >= 3:
				for f in range(2, len(header)):
					if header[f].lower() == "sum":
						row[header[0] + "_sum"] = soma(m_list)
					elif header[f] == "media":
						row[header[0] + "_media"] = soma(m_list) / len(m_list)
	return row



"""
 "123,pedro,12,12,12,miei"
[123,pedro,12,12,12,miei]
"""
def csv2json(file_name):
	file = open(file_name, "r", encoding="utf-8")
	make_headers(file)
	all_lines = file.readlines()
	row_list = []
	for line in all_lines:
		columns = re.finditer(r'([^,\n\t]*)(,|\n|\t)?', line)
		results = []
		for column in columns:
			results.append(column.group(1))
		row_list.append(build_row(results))
	# Write to json file
	out_file = open(file_name.replace(".csv", ".json"), "w", encoding="utf-8")
	out_file.write("[\n")
	for d in row_list:
		out_file.write("    {\n")
		for k in d:
			if type(d[k]) == str:
				out_file.write("        \"" + k + "\": \"" + str(d[k]) + "\",\n")
			else:
				out_file.write("        \"" + k + "\": " + str(d[k]) + ",\n")
		out_file.seek(out_file.tell() - 3)
		out_file.write("\n    },\n")
	out_file.seek(out_file.tell() - 3)
	out_file.write("\n]")
	out_file.close()


def run():
	if len(sys.argv) == 2:
		if exists(sys.argv[1]):
			csv2json(sys.argv[1])
			print("Done")
		else:
			print("File doesn't exist")
	else:
		print("Need a CSV file")


run()