import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Euler
def euler_step(x, h, F):
    return x + h * F(x)

def rk4_step(x, h, F):
    k1 = F(x)
    k2 = F(x + h/2 * k1)
    k3 = F(x + h/2 * k2)
    k4 = F(x + h * k3)
    return x + h/6 * (k1 + 2*k2 + 2*k3 + k4)

# ODE
def F(z):
    x, y = z
    return np.array([x - x**3, -y])

# Phase portrait
x = np.linspace(-2, 2, 25)
y = np.linspace(-2, 2, 25)
X, Y = np.meshgrid(x, y)

U = X - X**3
V = -Y

plt.figure(figsize=(5,5))
plt.quiver(X, Y, U, V)
plt.scatter([-1,0,1], [0,0,0], color='red')
plt.axis('equal')
plt.title("Phase portrait")
plt.show()

# Use of RK4
# def integrate(F, x0, h, steps):
#     traj = np.zeros((steps, len(x0)))
#     x = x0.copy()
#     for i in range(steps):
#         traj[i] = x
#         x = rk4_step(x, h, F)
#     return traj

# initial_conditions = [
#     np.array([0.2, 0.8]),
#     np.array([-0.2, -0.8]),
#     np.array([1.5, 0.5])
# ]

# plt.figure(figsize=(5,5))
# plt.quiver(X, Y, U, V, alpha=0.3)

# for x0 in initial_conditions:
#     traj = integrate(F, x0, 0.05, 300)
#     plt.plot(traj[:,0], traj[:,1])

# plt.axis('equal')
# plt.title("Integral curves")
# plt.show()

# Animation of particles
N = 300
x = np.random.uniform(-1.5, 1.5, N)
y = np.random.uniform(-1.5, 1.5, N)
dt = 0.05

fig, ax = plt.subplots(figsize=(5,5))
ax.set_xlim(-2,2)
ax.set_ylim(-2,2)
ax.set_aspect('equal')

particles = ax.scatter(x, y, s=20)

def update(frame):
    global x, y
    z = np.column_stack([x, y])
    dz = np.array([F(zi) for zi in z])
    z = z + dt * dz
    x, y = z[:,0], z[:,1]
    particles.set_offsets(z)
    return particles,

ani = FuncAnimation(fig, update, frames=300, interval=30)
plt.show()
