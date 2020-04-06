from decimal import Decimal
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from numpy import trapz

fail_rate = 1/150
correcting_rate = 1/4
preventing_rate = 1/1500
C = 0.8
dt = 0.01

area = plt.figure()

plot_r = area.add_subplot(1, 1, 1)

for cover in range (80, 101, 5):
    C = cover/100
    one_failed_covered = round(2*fail_rate*C*dt, 6)
    one_recovered = round(correcting_rate*dt, 6)
    two_failed = round(fail_rate*dt, 6)
    any_failed_not_covered = round(2*fail_rate*(1-C)*dt, 6)
    both_work = round(1 - one_failed_covered - any_failed_not_covered, 6)
    only_one_working = round(1 - one_recovered - two_failed, 6)
    two_recovered = round(correcting_rate*dt , 6)
    still_failed = round(1-two_recovered, 6)

    Tok =   [both_work,                 one_recovered,      two_recovered]
    Ook =   [one_failed_covered,        only_one_working,   0]
    F =     [any_failed_not_covered,    two_failed,         still_failed]

    M = np.array([Tok, Ook, F])
    E = np.array([[1],[0],[0]])
    I = np.identity(3)

    N = M
    found = False
    k = 0
    tempos = [k * dt]
    pf = 0
    pf_anterior = pf
    R = [1 - pf]
    while (found == False):

        N = M.dot(N)
        Q = N.dot(E)
        # print(Q)
        # print(round(Q[2][0], 6))
        pf = round(Q[2][0], 6)
        T = k * dt
        # plt.plot(T, round(1.000000 - round(Q[2][0], 6), 6), 'ro-')
        k += 1
        tempos.append(T)
        R.append(1 - pf)
        if (pf == pf_anterior):
            print(k)
            found = True
        pf_anterior = pf

    data = {'tempo': tempos, 'R': R}
    data_frame = pd.DataFrame(data,columns=['tempo', 'R'])
    print(data_frame)

    lines = plot_r.plot(data_frame.tempo.values, data_frame.R.values)
    plot_r.set_ylim(ymin=0.9)
    plot_r.set_xlim(xmin=0)
    lines[-1].set_label(f'C = {C}')


    # area_R = trapz(data_frame.R.values)
    # print(f"MTTF: {round(area_R, 2)}" )
    print(f"Assíntota: {data_frame.R.values[-1]}")
    print(f"Disponibilidade assintótica: {data_frame.R.values[-1]*100}%")
plot_r.legend()
area.savefig(f'rd.png', dpi = 300, bbox_inches = 'tight')
