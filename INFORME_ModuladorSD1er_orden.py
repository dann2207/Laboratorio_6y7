import matplotlib.pyplot as plt
import numpy as np

A_0 = 1 
f_0 = 0.5 
phi_0 = 0 
f_B = 1 
f_s = 100 
offsetDC_0 = 0

def signal(t,offsetDC=offsetDC_0,A=0.5*A_0,f=f_0,phi=phi_0):
    return offsetDC + A*np.sin(2*np.pi*f*t+phi)

X_FS = 2*A_0
g_q = 1 
Y_FS = g_q*X_FS
N_overload = 0

def q(x):
    global N_overload
    if np.abs(x)>X_FS/2:
        N_overload += 1 
    if x<0: 
        return -Y_FS/2
    else:
        return Y_FS/2

e_0 = Y_FS/2 
T_s = 1/f_s
N = 8192 
t = np.arange(0,N*T_s,T_s) 

def PlotPulsosSD(offsetDC=offsetDC_0,A=0.5*A_0,f=f_0,phi=phi_0,ids="xuvey"):
    x = signal(t,offsetDC=offsetDC,A=A,f=f,phi=phi)
    u = [x[0]-q(0)]
    r = [x[0]-q(0)]
    v = [0]
    e = [e_0]
    y = [q(0)]

    for n in range(1,N):
        V = x[n-1]-e[n-1]
        u.append(x[n]-q(V))
        r.append(x[n]-q(V)+V)
        v.append(V)
        e.append(q(V)-V)
        y.append(q(V))

    print("OVERLOADING: nos fuimos del rango X_FS del cuantizador {} veces".format(N_overload))
    print("A={}, f={}, phi={}".format(A,f,phi))

    plt.figure(figsize=(10, 3))

    if 'x' in ids: plt.plot(t,x,label='x',color="navy",linewidth=3,zorder=10)
    if 'u' in ids: plt.plot(t,u,label='u')
    if 'r' in ids: plt.plot(t,r,label='r')
    if 'v' in ids: plt.plot(t,v,label='v')
    if 'e' in ids: plt.plot(t,e,label='e')
    if 'y' in ids: plt.plot(t,y,label='y',marker="o",markersize=4,markerfacecolor="w",markeredgewidth=1.5,color="k",linewidth=.5)

    plt.xlabel("Tiempo [seg]")
    plt.ylabel("Amplitud [V]")
    plt.xlim(0,1/f_0)
    plt.grid()
    plt.legend(loc=(1.01,0.75))
    plt.show()

