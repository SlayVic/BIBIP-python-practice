# Task 1
![work](img/work.png)

## Пояснення
___
### Введення строки:
```py
line = input('Give me line to work: ')
```
___
### Розділення строки на слова:
```py
lineSplit = line.split()
```
___
### Діставання чисел з масиву:
```py
i = 0
while(i < len(lineSplit)):
    if lineSplit[i].isdecimal():
        numbers.append(int(lineSplit.pop(i)))
        continue
    digits = ''.join(filter(lambda i: i.isdecimal(), lineSplit[i]))
    if digits:
        numbers.append(int(digits))
        lineSplit[i] = ''.join(filter(lambda i: not i.isdecimal(), lineSplit[i]))
    i += 1
```

#### Внесення до спису чисел якщо весь елемент число:
```py
if lineSplit[i].isdecimal():
    numbers.append(int(lineSplit.pop(i)))
```

#### Внесення до спису чисел числа з середени слів:
```py
digits = ''.join(filter(lambda i: i.isdecimal(), lineSplit[i]))
    if digits:
        numbers.append(int(digits))
        lineSplit[i] = ''.join(filter(lambda i: not i.isdecimal(), lineSplit[i]))
```
```py
''.join()
```
потрібно щоб перевести результат фільтру у строку
___
### Капіталізація першої та останньої літтери слова:
```py
for i in range(len(lineSplit)):
    lineSplit[i] = lineSplit[i].title()[:-1] + lineSplit[i][-1].upper()
```
___
### Математичні маніпуляції, данні у умові, з числами, лише якщо числа є:
```py
if numbers:
    maxNumber = max(numbers)
    numbersPowered = list(map(lambda x: x ** numbers.index(x) if x != maxNumber else x, numbers))
```
___
### Перетворення масиву слів в строку:
```py
lineEdited = ' '.join(lineSplit)
```
___
### Виведення інформації, про числа лише якщо вони є:
```py
print('', f'Line: {line}', '',
      f'line after edit: {lineEdited}', '', sep="\n")

if numbers:
    print(f'gotten numbers: {numbers}', '',
          f'maximum number: {maxNumber}', '',
          f'numbers after powering: {numbersPowered}', sep="\n")
```

## Git commit:
![git commit](img/git-commit-in-console.png)