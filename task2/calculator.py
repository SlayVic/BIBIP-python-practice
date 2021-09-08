from math import *
import re
# import math


# * replace elements to make it more understandable
def simplify(expression):
    expression = expression.replace("Pi", "3.14159265359")
    expression = expression.replace("pi", "3.14159265359")

    expression = expression.replace("E", "2.7182818285")

    expression = expression.replace(",", ".")
    expression = expression.replace(";", ",")
    expression = expression.replace("plus", "+")
    expression = expression.replace("and", "+")
    expression = expression.replace("with", "+")

    expression = expression.replace("minus", "-")
    expression = expression.replace("subtract", "-")
    expression = expression.replace("without", "-")

    expression = expression.replace("times", "*")
    expression = expression.replace("multiplied by", "*")
    expression = expression.replace("mul", "*")
    expression = expression.replace("multiply", "*")

    expression = expression.replace("divide", "/")
    expression = expression.replace("divide by", "/")

    expression = expression.replace("ctg", "1/tan")
    expression = expression.replace("tg", "tan")

    ln = re.search(r'ln\([\w\d\+\-\*\/\.]+\)', expression)
    while ln:
        ln_in_future = ln[0]
        ln_in_future = 'log('+ln_in_future[3:-1]+','+'2.7182818285)'
        expression = expression.replace(ln[0], ln_in_future)
        ln = re.search(r'ln\([\w\d\+\-\*\/\.]+\)', expression)

    lg = re.search(r'lg\([\w\d\+\-\*\/\.]+\)', expression)
    while lg:
        lg_in_future = lg[0]
        lg_in_future = 'log('+lg_in_future[3:-1]+','+'10)'
        expression = expression.replace(lg[0], lg_in_future)
        lg = re.search(r'lg\([\w\d\+\-\*\/\.]+\)', expression)

    percent = re.search(r'[\+\-]\d+\.?\d*%', expression)
    while percent:
        percent_in_future = percent[0]
        percent_in_future = '*'+str(eval(f'1{percent_in_future[:-1]}/100'))
        expression = expression.replace(percent[0], percent_in_future)
        percent = re.search(r'[\+\-\*\/]\d+\.?\d*%', expression)

    percent = re.search(r'\d+\.?\d*%', expression)
    while percent:
        percent_in_future = percent[0]
        percent_in_future = str(eval(f'{percent_in_future[:-1]}/100'))
        expression = expression.replace(percent[0], percent_in_future)
        percent = re.search(r'[\+\-\*\/]\d+\.?\d*%', expression)

    fact = re.search(r'\d+\.?\d*\!', expression)
    while fact:
        fact_in_future = fact[0]
        fact_in_future = 'factorial('+fact_in_future[:-1]+')'
        expression = expression.replace(fact[0], fact_in_future)
        fact = re.search(r'\d+\.?\d*!', expression)

    expression = expression.replace(" ", "")
    print(expression)
    return expression


# * Search all function in expression without function inside
def searchFunction(expression, text_of_func, func):
    while(True):  # * loop to search all
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


# * list of functions
functions = [('cos', cos), ('sin', sin), ('tan', tan),
             ('log', log), ('factorial', factorial), ('sqrt', sqrt)]


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


# * debug
if __name__ == "__main__":
    expression = "ln(sin(E))"

    print(calculate(expression))
