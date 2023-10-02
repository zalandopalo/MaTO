import math
import sys
from scipy import optimize
from sympy import *
from sympy.plotting import plot
import numpy as np
from matplotlib import pyplot as plt


def duplicator(fx: str, vary: list = None, substitute: list = None) -> [str, str]:
    """
    Input Function u want to duplicate. Get 2 for sale.
    By default, returns duplicate with "variable_name1"
    Subsequence in vary and substitute must be same.
    :param fx: Function for duplicating
    :param vary: list of variables, you want to rename
    :param substitute: list of new names for variables.
    :return: 2 functions
    """
    if vary is None and substitute is None:
        variables = symbol_search(fx)
        fx1 = fx
        new_var = ""
        for elem in fx.split(" "):
            if (elem in variables) and (elem not in new_var):
                fx1 = fx.replace(f'{elem}', f'{elem}1')
                new_var += elem
            else:
                continue
        return fx, fx1
    elif vary is not None and substitute is not None:
        fx1 = fx
        new_var = ""
        for elem in fx.split(" "):
            if (elem in vary) and (elem not in new_var):
                fx1 = fx.replace(f'{elem}', f'{substitute[vary.index(elem)]}')
                new_var += elem
            else:
                continue
        return fx, fx1
    else:
        fx1 = fx
        new_var = ""
        variables = symbol_search(fx)
        for elem in fx.split(" "):
            if (elem in variables) and (elem not in new_var):
                fx1 = fx.replace(f'{elem}', f'{substitute[variables.index(elem)]}')
                new_var += elem
            else:
                continue
        return fx, fx1


def preparator(fx: str) -> str:
    """
    All inputting functions needs to be prepared for use
    :param fx:  Function
    :return: prepared function for eval()
    """
    opers = ["sqrt(", "exp", "pi", "e(", "cos(", "sin(", "asin(", "acos(", "tan(", "atan("]
    for elem in fx.split(" "):
        if elem in opers:
            fx = fx.replace(f'{elem}', f'math.{elem}')
        else:
            continue
    return fx


def symbol_search(string: str) -> str:
    """
    :param string:  separated with spaces function
    :return: sorted string with variables
    """
    values = ''
    s = ".,:;!_*-+()/#%&"

    for value in string.split(' '):
        if value.isalpha():
            if value not in values:
                values += value
        elif value in s:
            continue
        else:
            continue
    return ", ".join(sorted(values))


def alg_svenn(start_location, step, fx):
    """
    Svenn's Algorithm
    :param start_location: Start point
    :param step: Step
    :param fx: Function sympy
    :return: Minimum localization interval
    """
    x0 = start_location
    h = step
    function = fx
    # вычислить функцию по значению х
    function = preparator(function)
    function, function1 = duplicator(function)

    function = compile(function, "<string>", "eval")
    function1 = compile(function1, "<string>", "eval")
    # проверка на направление функции
    x, x1 = x0, x0 + h
    fx1 = round(float(eval(function)), 3)
    fx2 = round(float(eval(function1)), 3)
    flag = (fx1 < fx2)
    if flag == True:
        h = 0 - h
        x1 = x0 + h
        fx2 = round(float(eval(function1)), 3)
    else:
        x1 = x + (2 * h)
        fx2 = round(float(eval(function1)), 3)
    f = x
    flag1 = (fx1 < fx2)
    while flag1 == False:
        f = x
        x = x1
        h = round(h + h, 3)
        x1 = round(x1 + h, 3)
        fx1 = round(float(eval(function)), 3)
        fx2 = round(float(eval(function1)), 3)
        flag1 = (fx1 < fx2)
    interval_min = f
    interval_max = x1
    return [interval_min, interval_max]


def build_function(function: str) -> [float, float]:
    """
    main program thread
    """
    try:
        func = function
        # ввод операции

        oper_type = input("Input operation option\n(diff, local_ext): ")
        match oper_type.lower():
            #  для расширения функционала
            case "diff":
                dif_var = input("Differentiation by:")
                syms = symbol_search(function)
                globals()[syms] = symbols(syms)
                dfunc = diff(func, dif_var)
                return dfunc
            case "local_ext":
                alg = input("Select algorithm\n(Svens):")
                match alg.lower():
                    # Алгоритм Свенна
                    case "svens":  # 0.75 * ( x ** 4 ) - 2 * ( x ** 3) + 2
                        # Minimum localization interval

                        localiz = alg_svenn(0, 0.1, func)
                        plt.title(f"Method: {alg.upper()}\n Function: {func}")
                        plt.xlabel("X")
                        plt.ylabel("Y")
                        plt.grid()
                        plot_x = np.arange(min(localiz) - 5, max(localiz) + 5, 0.001)
                        plot_y = preparator(func)
                        _, plot_y = duplicator(plot_y, None, ["plot_x"])
                        plt_y = [eval(plot_y) for plot_x in plot_x]
                        plt.ylim(min(plt_y) - 1, 7)
                        plt.plot(plot_x, plt_y, "g-", label='Function')
                        plot_x1 = np.arange(min(localiz), max(localiz), 0.001)
                        plot_y1 = [0 for i in range(np.size(plot_x1))]

                        plt.plot(plot_x1, plot_y1, "r-", label='MLI')
                        plt.legend()
                        plt.show()

                        return localiz
                    case _:
                        print("No such method")
                        return None
            case _:
                print("No such operation")
                return None

    except:
        return eval(function)


while True:
    strings = input("Split values with ' ': ")
    match strings:
        case "exit":
            sys.exit(0)
        case _:
            print(build_function(strings))
