# Task 1
![work](https://user-images.githubusercontent.com/43368065/124328677-c4e54500-db92-11eb-961d-900dea61eb73.png)

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
lineSplit = list(map(lambda item: item.title()[:-1] + item[-1].upper(),lineSplit))
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
![git-commit-in-console](https://user-images.githubusercontent.com/43368065/124328691-ca428f80-db92-11eb-98ba-82027db5751a.png)
