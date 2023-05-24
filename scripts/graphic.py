import matplotlib.pyplot as plt 
import numpy as np 
from math import sin, cos


def graphic_module(fg):
    fig, ax = plt.subplots()
    ax. set_title ("График функции")
    ax.set_xlabel ('x')
    ax.set_ylabel('y')
    # Начало и конец изменения значения Х, разбитое на 100 точек
    x = np. linspace(-10, 10, 500) # X от -5 до 5
    y = [eval(f"{fg}") for x in x]

    ax.plot(x,y)
    plt.savefig("data/img/graphic.png")
    plt.close()
