# Task 2

![Working-program](img/Working-program.png)

## Explanation of [calculator.py](calculator.py), file that calculate answers

### Make input understandable for builded in python calculator

```py
expressio = expressio.replace("Pi", "3.14159265359")
expressio = expressio.replace("pi", "3.14159265359")

expressio = expressio.replace("E", "2.7182818285")

expressio = expressio.replace(",", ".")
expressio = expressio.replace(";", ",")
expressio = expressio.replace("plus", "+")
expressio = expressio.replace("and", "+")
expressio = expressio.replace("with", "+")

expressio = expressio.replace("minus", "-")
expressio = expressio.replace("subtract", "-")
expressio = expressio.replace("without", "-")

expressio = expressio.replace("times", "*")
expressio = expressio.replace("multiplied by", "*")
expressio = expressio.replace("mul", "*")
expressio = expressio.replace("multiply", "*")

expressio = expressio.replace("divide", "/")
expressio = expressio.replace("divide by", "/")

expressio = expressio.replace("ctg", "1/tan")
expressio = expressio.replace("tg", "tan")
expressio = expressio.replace(" ", "")
```

Next algorithms are using for find and change more complex math functions by using regex. F\*ck regex.

```py
ln = re.search(r'ln\([\w\d\+\-\*\/\.]+\)', expressio)
while ln:
    ln_in_future = ln[0]
    ln_in_future = 'log('+ln_in_future[3:-1]+','+'2.7182818285)'
    expressio = expressio.replace(ln[0], ln_in_future)
    ln = re.search(r'ln\([\w\d\+\-\*\/\.]+\)', expressio)
```

```py
lg = re.search(r'lg\([\w\d\+\-\*\/\.]+\)', expressio)
while lg:
    lg_in_future = lg[0]
    lg_in_future = 'log('+lg_in_future[3:-1]+','+'10)'
    expressio = expressio.replace(lg[0], lg_in_future)
    lg = re.search(r'lg\([\w\d\+\-\*\/\.]+\)', expressio)
```

```py
percent = re.search(r'[\+\-]\d+\.?\d*%', expressio)
while percent:
    percent_in_future = percent[0]
    percent_in_future = '*'+str(eval(f'1{percent_in_future[:-1]}/100'))
    expressio = expressio.replace(percent[0], percent_in_future)
    percent = re.search(r'[\+\-\*\/]\d+\.?\d*%', expressio)
```

```py
percent = re.search(r'\d+\.?\d*%', expressio)
while percent:
    percent_in_future = percent[0]
    percent_in_future = str(eval(f'{percent_in_future[:-1]}/100'))
    expressio = expressio.replace(percent[0], percent_in_future)
    percent = re.search(r'[\+\-\*\/]\d+\.?\d*%', expressio)
```

```py
fact = re.search(r'\d+\.?\d*\!', expressio)
while fact:
    fact_in_future = fact[0]
    fact_in_future = 'factorial('+fact_in_future[:-1]+')'
    expressio = expressio.replace(fact[0], fact_in_future)
    fact = re.search(r'\d+\.?\d*!', expressio)
```

### function that search and calculate functions

`'\*' in comments need to make it green in my editor, never mind. `

```py
# * Search all function in expression without function inside
def searchFunction(expression, text_of_func, func):
    while(True):  # * loop to search all
        isEndFirst = False

        # * regex to search function
        #! f*ck regex.
        found = re.search('{}'.format(text_of_func) +
                          r'\(([^\(\)\D]|,|\.|\+|\*|\/|-)*\)', expression)
        if found:  # * if found
            step = found[0][len(text_of_func)+1:-1]  # * get funcion variables
            # * split if have 2 instead of 1 line in log, it only for log
            steps = step.split(',')
            print(steps)    # print step in console for debug
            stepAnswer = 0
            # * get answer of funcion by using eval
            if len(steps) <= 1:
                stepAnswer = str(func(eval(steps[0])))
            else:
                stepAnswer = str(func(eval(steps[0]), float(steps[1])))
            # * Print for debug
            print(f'{text_of_func}({step}) = {stepAnswer}')
            # * Edit expression with result
            expression = expression.replace(
                f'{text_of_func}({step})', stepAnswer)
        else:  # * if not found anything exit from function
            print(f"No steps for {text_of_func}()")
            return expression
```

### list of supported math functions, can be modified in any time

```py
# * list of functions
functions = [('cos', cos), ('sin', sin), ('tan', tan),
             ('log', log), ('factorial', factorial), ('sqrt', sqrt)]
```

### function that get expression and use math functions for it

```py
# * Function that calculate expression
def calculate(expression):
    was = ''  # * old expression
    try:
        while expression != was:
            expression = simplify(expression)  # * make expression simple
            was = expression  # * save as old expression
            for func in functions:  # * search all functions in expression
                expression = searchFunction(expression, func[0], func[1])

        # * search highest brackets expression
        while True:
            # * by f*cking regex
            found = re.search(r'\([^\(\)]*\)', expression)
            if found:
                step = found[0][1:-1]  # * step without brackets
                stepAnswer = str(eval(step))  # * calculate by eval
                print(f'({step}) = {stepAnswer}')  # * print step for debug
                # * change old step with step answer
                expression = expression.replace(f'({step})', stepAnswer)
            else:  # * when not having brackets
                print("No steps for ()")
                break  # * exit from loop
        # * return calculated func in case if final expression have +-*/ but not in brackets
        return eval(expression)
    except:  # * if something get wrong
        return 'Cant'
```

## Explanation of [main.py](main.py), file with application

### import **tk** and function **calculate** from [calculator.py](calculator.py)

```py
import tkinter as tk
from calculator import calculate
```

### create window
```py
root = tk.Tk()
root.geometry('597x507')  # * size
root.minsize(597, 507)  # * min size
root.resizable(True, False)  # * resize lock
root.title('Shashkov inline calculator')  # * title
app = Application(master=root)  # * start class
app.mainloop()  # * start program work
```

### **\_\_init__**, starter for application

```py
def __init__(self, master=None):
    super().__init__(master)

    self.master = master
    # * event on changing size to chage output box size
    self.master.bind('<Configure>', self.set_sizes)
    self.input = tk.Text(self.master)  # * create textBox
    # * create output box on right side
    self.output = tk.Message(self.master)
    self.configure_widgets()  # * configure widgets
```

### configure widgets

```py
def configure_widgets(self):
    self.input.pack(side=tk.LEFT)  # * pack on the left side
    self.input['height'] = self.height  # * set sizes
    self.input['width'] = self.width    # * set sizes
    self.master.update()  # * update window
    self.input['font'] = ("Arial", 14)  # * set font
    self.input.bind('<Key>', self.calculate)  # * make event on key press

    # * pack output widget next to input textbox
    self.output.pack(side=tk.LEFT)
    self.output['font'] = ("Arial", 14)  # * set font
    self.set_sizes()  # * set output sizes
```

### **set_sizes**, set size for output widget

```py
def set_sizes(self, *tmp):
    self.master.update()
    # * output box fill extra space next to text box
    self.output['width'] = self.master.winfo_width()-10 - \
        self.input.winfo_width()
```

### **calculate**, use calculate func from [calculator.py](calculator.py) to get answer for all lines

```py
# * get answers
def calculate(self, *tmp):
    text = self.input.get("1.0", tk.END)[:-1]  # * get text without \n
    # * add pressed key character 'couse tkinter suck.
    if tmp[0].char:
        text += tmp[0].char

    height = self.height-1  # * counter of how much lines need
    lines = text.split('\n')
    end_text = ''

    # * calculate each line
    for line in lines:
        if not line.startswith('bin'):  # * for binary conversion
            # * if not bin
            end_text += str(calculate(line))+'\n'
        else:  # * bin
            try:
                # * send line without bin and remove 0b from bin() return
                end_text += bin(calculate(line[3:]))[2:]+'\n'
            except:  # * if cant get bin, like in float numbers
                end_text += "Cant\n"
        height -= 1  # * -1 void line
    end_text += '\n'*height  # * add void lines to align widget right
    self.output['text'] = end_text  # * change output widget text

```

## Binary

Sorry, I made not button for binary because my calculator inline, so I make command for binary
![binary-showcase](img/binary.png)
