# We want to animate a vector field using matplotlib's quiver and FuncAnimation.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# number of particles
N = 5000

# initial positions (random)
x = np.random.uniform(-1.5, 1.5, N)
y = np.random.uniform(-1.5, 1.5, N)

fig, ax = plt.subplots()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
particles = ax.scatter(x, y, s=20)

def F(x, y):
    return -5 * np.exp(-x**2 - y**2), y * np.exp(-x**2 - y**2)

dt = 0.005

def update(frame):
    global x, y

    vx, vy = F(x, y)

    x = x + dt * vx
    y = y + dt * vy

    particles.set_offsets(np.column_stack([x, y]))

    return particles,

ani = FuncAnimation(fig, update, frames=200, interval=50)
plt.show()