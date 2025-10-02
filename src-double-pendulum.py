import numpy as np
import matplotlib.pyplot as plt

#info en el S.I.
m1=1    
m2=1    
l1= 1   
l2= 1   
g =9.8   
#Cond. iniciales, porque quiero sol. unica
theta1_0=np.radians(120)
omega1_0=0
theta2_0=np.radians(-10)
omega2_0=0
# tamaño de paso en segundos
dt = 0.01      
#tiempo total
t_total = 20      

# ECUACIONES, se despeja theta dot dot desde el lagrangiano

def despejar_aceleracion(y):
    theta1, omega1, theta2, omega2=y
    delta_theta = theta1 - theta2
    denom1 = (2*m1 + m2 - m2 * np.cos(2*delta_theta))*l1
    theta1_dot = omega1
    num1 =-2*m2*np.sin(delta_theta)*(omega2**2*l2+omega1**2*l1*np.cos(delta_theta))-g*(2*m1 + m2)*np.sin(theta1)-m2*g*np.sin(theta1-2*theta2)
    omega1_dot = num1/denom1
    theta2_dot = omega2
    denom2 = (2*m1 + m2 - m2 * np.cos(2*delta_theta))*l2
    num2 = 2*np.sin(delta_theta)*(omega1**2*l1*(m1+m2)+g*(m1+m2)*np.cos(theta1)+ omega2**2 * l2 * m2 * np.cos(delta_theta))
    omega2_dot=num2/denom2

    return np.array([theta1_dot, omega1_dot, theta2_dot, omega2_dot])

# RUNGE KUTTA
#### theta1, omega1, theta2, omega2=y
def rk4(y,dt):
    
    k1 = despejar_aceleracion(y)
    k2 = despejar_aceleracion(y+0.5*dt*k1)
    k3 = despejar_aceleracion(y+0.5*dt*k2)
    k4 = despejar_aceleracion(y+dt*k3)
    return y + (dt/6)*(k1+2*k2+2*k3+k4)

# SIMULACION
times=np.arange(0, t_total,dt)
N=len(times)
y=np.zeros((N,4))

# desde el estado inicial
y[0]=np.array([theta1_0,omega1_0,theta2_0,omega2_0])

for i in range(1,N):
    y[i]=rk4(y[i-1],dt)


def energy(y):
    theta1, omega1, theta2, omega2 = y.T
    K = 0.5*m1*(l1*omega1)**2 + 0.5*m2*( (l1*omega1)**2 + (l2*omega2)**2 + 2*l1*l2*omega1*omega2*np.cos(theta1-theta2) )
    U = -(m1+m2)*g*l1*np.cos(theta1) - m2*g*l2*np.cos(theta2)
    return K + U
#
E = energy(y)
if __name__ == "__main__":
    plt.figure()
    plt.plot(times, E)
    plt.xlabel('t (s)')
    plt.ylabel('Total energy (J)')
    plt.title('Energy (should be roughly constant for small dt)')
    plt.grid(True)
    plt.show()