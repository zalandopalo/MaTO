import math
import sys
from scipy import optimize
from sympy import *
from sympy.plotting import plot
import numpy as np
from matplotlib import pyplot as plt
import re


class Function:
    def __init__(self, fx: str):
        self.fx = fx
        self.fx = self.preparator()
        self.interval = self.alg_Swann()

    def __repr__(self):
        return f"{self.fx!r}"

    def preparator(self, fx: str = None) -> str:
        """
        All inputting functions needs to be prepared for use
        :return: prepared function for eval()
        """
        opers = ["sqrt(", "exp", "pi", "e(", "cos(", "sin(", "asin(", "acos(", "tan(", "atan("]
        if fx is None:
            fx = self.fx
        for elem in fx.split(" "):
            if elem in opers:
                fx = fx.replace(f'{elem}', f'math.{elem}')
            else:
                continue
        return fx

    def duplicator(self, fx: str = None, vary: list = None, substitute: list = None) -> [str, str]:
        """
        Input Function u want to duplicate. Get 2 for sale.
        By default, returns duplicate with "variable_name1"
        Subsequence in vary and substitute must be same.
        :param fx: Function for duplicating
        :param vary: list of variables, you want to rename
        :param substitute: list of new names for variables.
        :return: 2 functions
        """
        if fx is None:
            fx = self.fx
        fx1 = fx
        new_var = ""
        if vary is None and substitute is None:
            variables = self.symbol_search(fx)
            for elem in fx.split(" "):
                if (elem in variables) and (elem not in new_var):
                    fx1 = fx.replace(f'{elem}', f'{elem}1')
                    new_var += elem
                else:
                    continue
            return fx, fx1
        elif vary is not None and substitute is not None:
            for elem in fx.split(" "):
                if (elem in vary) and (elem not in new_var):
                    fx1 = fx.replace(f'{elem}', f'{substitute[vary.index(elem)]}')
                    new_var += elem
                else:
                    continue
            return fx, fx1
        else:
            variables = self.symbol_search(fx)
            for elem in fx.split(" "):
                if (elem in variables) and (elem not in new_var):
                    fx1 = fx.replace(f'{elem}', f'{substitute[variables.index(elem)]}')
                    new_var += elem
                else:
                    continue
            return fx, fx1

    def symbol_search(self, string: str) -> str:
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

    def golden_ratio(self, fx: str = None, interval: [] = None, accuracy: float = 0.01):
        """
        Golden ratio method.
        :param fx: function to use
        :param interval: list [min, max], default = Swann's alg .
        :param accuracy: minimum size of interval.
        :return: Interval, middle point of interval.
        """
        if interval is None:
            interval = self.interval
        else:
            interval = interval
        if fx is None:
            fx = self.fx

        a, b = float(interval[0]), float(interval[1])
        function = compile(fx, "<string>", "eval")

        loca = abs(a - b)
        y = a + 0.38196 * (b - a)
        z = a + b - y
        while loca > accuracy:
            fyk = round(eval(function, {"x": y}), 4)
            fzk = round(eval(function, {"x": z}), 4)

            if fyk <= fzk:
                b = z
                z = y
                y = a + (b - y)

            else:
                a = y
                y = z
                z = a + (b - z)
            loca = abs(a - b)
        mid_point = ((a + b) / 2)
        GraphicPls.graphic(self, name="Golden ratio ", fx=fx, interval=[round(a, 4), round(b, 4)],
                           point=round(mid_point, 4))
        return [round(a, 4), round(b, 4)], round(mid_point, 4)

    def dichotomia(self, fx: str = None, interval: [] = None, accuracy: float = 0.01):
        """
        Dichotomia method.
        :param interval: list [min, max].
        :param accuracy: minimum size of interval.
        :return: Interval, middle point of interval.
        """
        if interval is None:
            interval = self.interval

        if fx is None:
            fx = self.fx

        a, b = float(interval[0]), float(interval[1])
        function = compile(fx, "<string>", "eval")
        # step 3
        mid_point = (b + a) / 2
        fmid = eval(function, {"x": mid_point})
        # step 4
        while (b - a) > accuracy:
            delta = (abs(b - a)) / 4
            yk, zk = a + delta, b - delta
            fyk, fzk = eval(function, {"x": yk}), eval(function, {"x": zk})
            if round(fyk, 4) < round(fmid, 4):
                b = mid_point
                mid_point = (b + a) / 2
                fmid = eval(function, {"x": mid_point})
            else:
                if round(fzk, 4) < round(fmid, 4):
                    a = mid_point
                    mid_point = (b + a) / 2
                    fmid = eval(function, {"x": mid_point})
                else:
                    a, b = yk, zk
                    mid_point = (b + a) / 2
                    fmid = eval(function, {"x": mid_point})

        GraphicPls.graphic(self, name="Dichotomia", fx=fx, interval=[round(a, 4), round(b, 4)],
                           point=round(mid_point, 4))
        return [round(a, 4), round(b, 4)], round(mid_point, 4)

    def uni_search(self, n: int = 10, fx: str = None, interval: [] = None):
        """
        line search.
        :param fx: function to use.
        :param interval: list [min, max].
        :param n: Number of interval splits.
        :return: Interval, middle point of interval.
        """
        if interval is None:
            interval = self.interval
        else:
            interval = interval
        if fx is None:
            fx = self.fx

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
        GraphicPls.graphic(self, name="uni. search", fx=fx, interval=mit, point=min_point)
        return mit, min_point

    def alg_Swann(self, start_location=0, step=0.01, fx: str = None):
        """
        Svenn's Algorithm
        :param fx: additional function
        :param start_location: Start point
        :param step: Step
        :return: Minimum localization interval
        """
        if fx is None:
            fx = str(self.fx)

        x0 = start_location
        h = step
        # вычислить функцию по значению х
        function, function1 = self.duplicator(fx=fx)
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
        return sorted([interval_min, interval_max])


class GraphicPls(Function):

    def graphic(self, name: str, fx: str = None, interval: [] = None, point: float = None):
        plt.title(f"Method: {name}\n Function: {fx}")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid()
        plot_x = np.arange(min(interval) - 2, max(interval) + 2, 0.001)
        plot_y = self.preparator(fx)
        plt_y = [eval(plot_y) for x in plot_x]
        plt.ylim(min(plt_y) - 1, min(plt_y) + 4)
        plt.plot(plot_x, plt_y, "g-", label='Function')
        plot_x1 = np.arange(min(interval), max(interval), 0.001)
        plot_y1 = [eval(plot_y) for x in plot_x1]
        plt.plot(plot_x1, plot_y1, "r-", label=f'MLI: {interval}\nMIP: {point}')

        if point is not None:
            plt.scatter(point, eval(plot_y, {"x": point}))
        plt.legend()
        plt.show()


fx = Function("0.75 * ( x ** 4 ) - 2 * ( x ** 3) + 2")
print(fx.dichotomia())
