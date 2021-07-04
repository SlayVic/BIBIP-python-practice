from math import *
import re
# import math


def simplify(expressio):
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

    ln = re.search(r'ln\([\w\d\+\-\*\/\.]+\)', expressio)
    while ln:
        ln_in_future = ln[0]
        ln_in_future = 'log('+ln_in_future[3:-1]+','+'2.7182818285)'
        expressio = expressio.replace(ln[0], ln_in_future)
        ln = re.search(r'ln\([\w\d\+\-\*\/\.]+\)', expressio)

    lg = re.search(r'lg\([\w\d\+\-\*\/\.]+\)', expressio)
    while lg:
        lg_in_future = lg[0]
        lg_in_future = 'log('+lg_in_future[3:-1]+','+'10)'
        expressio = expressio.replace(lg[0], lg_in_future)
        lg = re.search(r'lg\([\w\d\+\-\*\/\.]+\)', expressio)

    percent = re.search(r'[\+\-]\d+\.?\d*%', expressio)
    while percent:
        percent_in_future = percent[0]
        percent_in_future = '*'+str(eval(f'1{percent_in_future[:-1]}/100'))
        expressio = expressio.replace(percent[0], percent_in_future)
        percent = re.search(r'[\+\-\*\/]\d+\.?\d*%', expressio)

    percent = re.search(r'\d+\.?\d*%', expressio)
    while percent:
        percent_in_future = percent[0]
        percent_in_future = str(eval(f'{percent_in_future[:-1]}/100'))
        expressio = expressio.replace(percent[0], percent_in_future)
        percent = re.search(r'[\+\-\*\/]\d+\.?\d*%', expressio)

    fact = re.search(r'\d+\.?\d*\!', expressio)
    while fact:
        fact_in_future = fact[0]
        fact_in_future = 'factorial('+fact_in_future[:-1]+')'
        expressio = expressio.replace(fact[0], fact_in_future)
        fact = re.search(r'\d+\.?\d*!', expressio)

    expressio = expressio.replace(" ", "")
    print(expressio)
    return expressio


def searchFunction(expressio, text_of_func, func):
    while(True):
        isEndFirst = False

        found = re.search('{}'.format(text_of_func) +
                          r'\(([^\(\)\D]|,|\.|\+|\*|\/|-)*\)', expressio)
        if found:
            step = found[0][len(text_of_func)+1:-1]
            steps = step.split(',')
            print(steps)
            stepAnswer = 0
            if len(steps) <= 1:
                stepAnswer = str(func(eval(steps[0])))
            else:
                stepAnswer = str(func(eval(steps[0]), float(steps[1])))
            print(f'{text_of_func}({step}) = {stepAnswer}')
            expressio = expressio.replace(
                f'{text_of_func}({step})', stepAnswer)
        else:
            isEndFirst = True
            print(f"No steps for {text_of_func}()")

        if isEndFirst:
            break
    return expressio



functions = [('cos', cos), ('sin', sin), ('tan', tan),
             ('log', log), ('factorial', factorial),('sqrt',sqrt)]


def calculate(expressio):
    expressio = simplify(expressio)
    was = ''
    try:
        while expressio != was:
            was = expressio
            for func in functions:
                expressio = searchFunction(expressio, func[0], func[1])
        
        while True:
            found = re.search(r'\([^\(\)]*\)', expressio)
            if found:
                step = found[0][1:-1]
                stepAnswer = str(eval(step))
                print(f'({step}) = {stepAnswer}')
                expressio = expressio.replace(f'({step})', stepAnswer)
            else:
                print("No steps for ()")
                break
        return eval(expressio)
        # if re.match(r'\d+\.?\d*', expressio):
        #     pass
    except:
        return 'Cant'


if __name__ == "__main__":
    expressio = "sin(ln(E))"

    print(calculate(expressio))
    # print()
