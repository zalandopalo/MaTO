import math
import sys
from scipy import optimize
from sympy import *
from sympy.plotting import plot
import numpy as np
from matplotlib import pyplot as plt
import re


def dichotomia(fx: str, interval: [], accuracy: float):
    interval = sorted(interval)
    a, b = float(interval[0]), float(interval[1])
    delta = (abs(a) + abs(b)) / 4
    k = 0
    x_mid = (a + b) / 2

    return None, None


def uni_search(fx: str, interval: [], n: int):
    interval = sorted(interval)
    function, xi, a0, b0, = fx, [], int(interval[0]), int(interval[1])
    fxi = []
    function = compile(function, "<string>", "eval")
    for i in range(n):
        xi.append(a0 + (i + 1) * ((b0 - a0) / (n + 1)))
        x = xi[i]
        fxi.append(eval(function))
    min_point = round(xi[fxi.index(min(fxi))], 3)
    try:
        try:
            mit = [round(xi[fxi.index(min(fxi)) - 1], 3), round(xi[fxi.index(min(fxi)) + 1], 3)]
        except:
            mit = [round(xi[fxi.index(min(fxi)) - 1], 3), b0]
    except:
        mit = [a0, round(xi[fxi.index(min(fxi)) + 1], 3)]
    return min_point, mit


def alg_Swann(start_location, step, fx):
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


def graphic_pls(fx: str, name: str, interval: [] = None, point: float = None) -> None:
    if interval is None:
        interval = [-1, 1]
    plt.title(f"Method: {name}\n Function: {fx}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid()
    plot_x = np.arange(min(interval) - 2, max(interval) + 2, 0.001)
    plot_y = preparator(fx)
    plt_y = [eval(plot_y) for x in plot_x]
    plt.ylim(min(plt_y) - 1, min(plt_y) + 4)
    plt.plot(plot_x, plt_y, "g-", label='Function')
    plot_x1 = np.arange(min(interval), max(interval), 0.001)
    plot_y1 = [eval(plot_y) for x in plot_x1]
    plt.plot(plot_x1, plot_y1, "r-", label='MLI')

    if point is not None:
        plt.scatter(point, eval(plot_y, {"x": point}))
    plt.legend()
    plt.show()


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


def build_function(function: str) -> [float, float]:
    """
    main program thread
    """
    try:
        func = function
        # ввод операции

        oper_type = "local_min"  # input("Input operation option\n(diff, local_min): ")
        match oper_type.lower():
            #  для расширения функционала
            case "diff":
                dif_var = input("Differentiation by:")
                syms = symbol_search(function)
                globals()[syms] = symbols(syms)
                dfunc = diff(func, dif_var)
                return dfunc
            case "local_min":
                alg = "dichotomia"  # input("Select algorithm\n(Swann, uni_srch):")
                match alg.lower():
                    # Алгоритм Свенна
                    case "swann":  # 0.75 * ( x ** 4 ) - 2 * ( x ** 3) + 2
                        # Minimum localization interval
                        localiz = alg_Swann(1, 0.01, func)
                        graphic_pls(func, "Swann", localiz)
                        return localiz
                    case "uni_srch":
                        # uniform search
                        variant = input('input interval manually or use Swann method? (Manual/Swann:):')
                        match variant.lower():
                            case "manual":
                                interval = input("Input interval: 'from : to' :")
                                interval = re.split(" : | | :|: |:", interval)

                                point_min, localiz = uni_search(func, interval,
                                                                int(round(((abs(int(interval[0])) + abs(
                                                                    int(interval[1]))) * 10), 0)))
                                graphic_pls(func, "uniform search", localiz, point_min)
                                return localiz, point_min
                            case "swann":
                                localiz = alg_Swann(0, 0.01, func)
                                point_min, localiz = uni_search(func, localiz,
                                                                int(round((localiz[0]) + abs(localiz[1]) * 10, 0)))
                                graphic_pls(func, "Uniform search", localiz, point_min)
                                return localiz, point_min

                    case "dichotomia":
                        localiz = alg_Swann(0, 0.01, func)
                        localiz, point_min = dichotomia(func, localiz, 0.01)
                        graphic_pls(func, "Dichotomia", localiz, point_min)
                        return localiz, point_min

                    case _:
                        print("No such method")
                        return None
            case _:
                print("No such operation")
                return None

    except:
        return print("something gone wrong")


while True:
    strings = "0.75 * ( x ** 4 ) - 2 * ( x ** 3) + 2"  # input("Split values with ' ': ")
    match strings:
        case "exit":
            sys.exit(0)
        case _:
            print(build_function(strings))
            sys.exit(0)
