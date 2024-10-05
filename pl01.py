import json

file = open("alunos.csv", "r", encoding="utf-8")

lines = file.readlines()

print("Lines: " + str(len(lines)))
print("Chars: " + str(len(file.read())))

campos = lines[0].split(",")
lines = lines[1:]
meds = []

for line in lines:
    fields = line.split(",")
    med = (int(fields[3]) + int(fields[4]) + int(fields[5]) + int(fields[6])) / 4
    if med >= 15:
        meds.append(med)

for line in lines:
    fields = line.split(",")
    i = 0
    if int(fields[3]) == 0 or int(fields[4]) == 0 or int(fields[5]) == 0 or int(fields[6]) == 0:
        i = i + 1

print("Nao entregue: " + str(i))
print("NumAlunos: " + str(len(meds)))

json_data = {}

alunos = []
for line in lines:
    fields = line.split(",")
    aluno = {}
    i = 0
    for campo in campos:
        aluno[campo] = fields[i][1:-1]
        i = i + 1
    alunos.append(aluno)
json_data["alunos"] = alunos

out = open("alunos.json", "w", encoding="utf-8")
out.write(json.dumps(json_data))