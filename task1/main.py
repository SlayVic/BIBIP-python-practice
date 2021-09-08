# * Створити програму, яка на вхід приймає рядок,
# * та виділяє з нього всі числа в окремий масив,
# * після чого програма друкує рядок без чисел.
# * I масив чисел. Змінити цей рядок таким чином,
# * щоб кожне слово в ньому,
# * починалось і закінчувалось великою літерою.
# * Знайти максимальне значення в масиві чисел,
# * а всі інші числа піднести до степеню
# * по їх індексу, та записати в інший масив.


line = input("Give me line to work: ")
lineSplit = line.split()
numbers = []

i = 0
while i < len(lineSplit):
    if lineSplit[i].isdecimal():
        numbers.append(int(lineSplit.pop(i)))
        continue
    digits = "".join(filter(lambda i: i.isdecimal(), lineSplit[i]))
    if digits:
        numbers.append(int(digits))
        lineSplit[i] = "".join(filter(lambda i: not i.isdecimal(), lineSplit[i]))
    i += 1

lineSplit = list(map(lambda item: item.title()[:-1] + item[-1].upper(), lineSplit))

maxNumber = 0
numbersPowered = []
if numbers:
    maxNumber = max(numbers)
    numbersPowered = list(
        map(lambda x: x ** numbers.index(x) if x != maxNumber else x, numbers)
    )

lineEdited = " ".join(lineSplit)

print("", f"Line: {line}", "", f"line after edit: {lineEdited}", "", sep="\n")

if numbers:
    print(
        f"gotten numbers: {numbers}",
        "",
        f"maximum number: {maxNumber}",
        "",
        f"numbers after powering: {numbersPowered}",
        sep="\n",
    )
