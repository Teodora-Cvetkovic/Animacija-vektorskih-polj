import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Create a figure and axes
fig, ax = plt.subplots()

# Create a grid of points
x = np.linspace(-2, 2, 20)
y = np.linspace(-2, 2, 20)
X, Y = np.meshgrid(x, y)

# Initial vector field
U = -Y
V = X

q = ax.quiver(X, Y, U, V)
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')

# Animation update function
def update(frame):
    t = frame * 0.1
    U = np.exp(-t) + t
    V = np.sin(t) + t
    q.set_UVC(U, V)
    return q,

# Create animation
ani = FuncAnimation(fig, update, frames=100, interval=5)

plt.figure()
plt.quiver(X, Y, U, V)
plt.axis('equal')
plt.show()
