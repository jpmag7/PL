import re

# Expressão regular aqui ↓
p = re.compile(r'\\\w+{([^}]+)}')

# A linha ↓
m_line = "\\tttt{zzzz} cdcdc \cmd{1234}"

# Escolher método ↓ (search, match, findall, finditer)
s = p.search(m_line)

if s:
	# Alterar função ↓ (groups(), group(0, 1, ...))
	print(s.group())
else:
	print("Não encontrou nada")


#21122121