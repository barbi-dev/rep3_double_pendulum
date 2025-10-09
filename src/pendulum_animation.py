import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from double_pendulum import l1,l2,m1,m2,y,dt,N

#para lagranfiano son coord generalizadas, pero
#para graficar se hacen coordenadas cartesianas
#escojo todos los elementos de la columna 0 y 2: theta1, theta2
x1=l1*np.sin(y[:,0])
y1=-l1*np.cos(y[:,0])
x2=x1+l2*np.sin(y[:,2])
y2=y1-l2*np.cos(y[:,2])
# ANIMACION
plt.style.use('dark_background')
fig, ax=plt.subplots(figsize=(7,7))
ax.set_aspect('equal')
ax.axis("off")

#plot limits
L=l1+l2
ax.set_xlim(-L-0.2, L+0.2)
ax.set_ylim(-L-0.7, L-0.7)
ax.set_title('Pendulo doble')
ax.grid(True, linestyle='--', alpha=0.3)

line,=ax.plot([], [], lw=3.5, zorder=3)
#ZORDER ORDENA LA SUPERPOSICION DE LOS OBJETOS EN EL PLANO Z
#EL PRIMERO ES EL MAS GRANDE
trace,=ax.plot([], [], lw=2.5, alpha=0.7,color='orange', zorder=2)
##en posicion solocamos (0,0) como placeholder nada mas
masa1=plt.Circle((0,0), 0.05*m1**(1/3), fc='orange', zorder=4)
masa2 = plt.Circle((0,0), 0.05*m2**(1/3), fc='orange', zorder=5)
ax.add_patch(masa1)
ax.add_patch(masa2)

# paras dejar rastro en la segunda masa, cuantos puntos se toman para el rastro
#si dt=0.01s puntos_rastro=tiempo/paso_de_tiempo = 3s/0.01s=300 puntos
trace_points = int(3/dt)  
#inicializo animacion
def init():
    line.set_data([], [])
    trace.set_data([], [])
    masa1.center = (0,0)
    masa2.center = (0,0)
    return line, trace, masa1, masa2

def animate(i):
    frame_x=[0,x1[i],x2[i]]
    frame_y=[0,y1[i],y2[i]]
    #dibuja la linea que conecta origen con m1 y m1 con m2:
    line.set_data(frame_x, frame_y)
    masa1.center=(x1[i],y1[i])
    masa2.center=(x2[i],y2[i])

    # update rastro de la masa2
    #para no tomar valores negativos
    start = max(0,i-trace_points)
    #dibuja la traza tromando solo los 300 ultimos puntos [i-trace_point:i]
    trace.set_data(x2[start:i],y2[start:i])

    return line, trace, masa1, masa2

anim = animation.FuncAnimation(fig, animate, frames=N, interval=dt*1000, blit=True, init_func=init)
anim.save("pendulo_doble3.gif", writer="pillow", fps=30)
# Show interactive window
plt.show()