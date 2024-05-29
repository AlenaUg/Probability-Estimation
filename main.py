import numpy as np
import matplotlib.pyplot as plt
import math
from tkinter import *
from random import randint

# Подбрасывание монеты
def flip_coin():
    return randint(0, 1)

# Эксперемент по подбрасыванию монеты N раз с подсчетом частот
def experiment(N):
    result = np.zeros(N)
    counter = 0
    for i in range(N):
        fc = flip_coin()
        if fc == 0:
            counter += 1
        result[i] = counter / (i + 1)
    return result

# Моделирование М серий эксперементов по подбрасыванию монеты N раз
def exp_serial(M, N):
    result = np.zeros((M, N))
    for i in range(M):
        result[i,] = experiment(N)
    return result

# Вычисление доверительного интервала
def conf_interval(vs, alpha):
    m = vs.shape[0]
    a = (1 - alpha) / 2
    m_down = int(m * a)
    m_up = m - m_down - 1

    sorted_vs = np.sort(vs, axis=0)

    return np.apply_along_axis(lambda x: np.array([x[m_down], x[m_up]]), 0, sorted_vs)

# Функция вычисления средней частоты по столбцам
def mean(vs):
    return np.mean(vs, axis=0)

# Вычесление квантеля нормального распределения
def normal_quantile(p):
    return 4.91 * (p ** 0.14 - (1 - p) ** 0.14)

def clicked():
    N = int(txt.get())
    M = int(txt1.get())
    ALPHA = float(txt2.get())

    plt.xscale('log')  # Выставление логорифмитического маштаба
    vs = exp_serial(M, N)
    confidence_interval = conf_interval(vs, ALPHA)

    # График зависимсти частоты от подбрасывания для каждой серии
    for i in range(M):
        plt.plot(range(1, N + 1), vs[i], color='black')

    # Дверительный интервал
    plt.plot(range(1, N + 1), confidence_interval[0,], color="blue")
    plt.plot(range(1, N + 1), confidence_interval[1,], color="blue")

    # Средняя частота
    plt.plot(range(1, N + 1), mean(vs), color="red")
    plt.show()


    # График ошибки
    exp_error = (confidence_interval[1,] - confidence_interval[0,]) / 2  # Зависимость экспериментальной ошибки от кол-ва подбрас монеты
    coef = normal_quantile((1 + ALPHA) / 2)  # Теоретическая ошибка частоты от кол-ва подбрас. монеты
    theory_error = np.zeros(N)

    for i in range(1, N + 1):
        theory_error[i - 1] = coef * math.sqrt(0.5 * 0.5 / i)

    plt.xscale('log')

    plt.plot(range(1, N + 1), theory_error, color="blue")
    plt.plot(range(1, N + 1), exp_error, "r--")
    plt.show()


# Интерфейс
window = Tk()
window.title("Вероятность выпадения орла")

window.geometry('700x350')

frame = Frame(window, padx=100, pady=100)
frame.pack(expand=True)

lbl = Label(window, text="Введите кол-во подрасываний монеты: ", font=("Times New Roman", 16))
lbl.place(x=90, y=70)

txt = Entry(window, width=10)
txt.place(x=452, y=76)
txt.focus()

lbl1 = Label(window, text="Введите кол-во серий экспериментов: ", font=("Times New Roman", 16))
lbl1.place(x=90, y=110)

txt1 = Entry(window, width=10)
txt1.place(x=452, y=116)

lbl2 = Label(window, text="Введите доверительную вероятность α: ", font=("Times New Roman", 16))
lbl2.place(x=90, y=150)

txt2 = Entry(window, width=10)
txt2.place(x=452, y=156)

btn = Button(window, text="Расчитать", command=clicked, font=("Times New Roman", 16))
btn.place(x=300, y=250)

window.mainloop()
