import time
import numpy as np
import matplotlib.pyplot as plt
import Calculations as Calc


def ts(s, inside_iter, file_to_read, file_to_save, allow_zeros=False, headers=False, init_swap=False):
    """
    :param allow_zeros:
        bool, if true, allows TS to make swaps that result in no change in overall time
    :param init_swap:
        bool, if true, swaps loaded from file solution
    :param headers:
        bool, if true, deletes headers
    :param s:
        int, how many iterations are swaps blocked
    :param inside_iter:
        int, how many swaps to make
    :param file_to_read:
        string, directory to read from
    :param file_to_save:
        string, directory to save to
    :return:
        Saves matrix calculated by TS algorithm
    """
    m = np.genfromtxt(file_to_read, delimiter=',')
    if headers:
        m = m[1:][:]
    if init_swap:
        solution = Calc.initrandomswap_m(m)
    else:
        solution = m
    print(Calc.calculate_time_matrices(m))
    tabu_list = np.zeros((len(m), len(m)))
    times = []
    for i in range(1, inside_iter):
        start = time.time()
        print(i)
        tm = Calc.calculate_time_matrices(solution)
        times.append(tm)
        print(tm)
        move = Calc.calculate_moves2(solution, tabu_list, allow_zeros)
        print(move)
        solution = Calc.swap(solution, move[0], move[1])
        tabu_list = Calc.update_tabu_list(tabu_list)
        tabu_list[move[0], move[1]] = s
        print("time per inside iter :", time.time() - start)
    np.savetxt(file_to_save, solution, delimiter=",")
    print("FINAL FOR ", s, "BLOCKS ", inside_iter, "INSIDE ITERATIONS ", "SAVED TO ", file_to_save)
    plt.plot(times)
    plt.ylabel("czas")
    save = file_to_save + ".jpeg"
    plt.savefig(save)


# sample use
ts(s=12,
   inside_iter=100,
   file_to_read="dane3.csv",
   file_to_save='dane3TS.csv',
   allow_zeros=True,
   headers=True,
   init_swap=True)
