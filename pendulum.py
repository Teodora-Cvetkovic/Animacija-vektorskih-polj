import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Vector field
def F(z):
    q, p = z[:, 0], z[:, 1]
    return np.column_stack([p, -np.sin(q)])

# Euler step
def step(z, dt):
    q, p = z[:, 0], z[:, 1]
    p_new = p - dt * np.sin(q)
    q_new = q + dt * p_new
    return np.column_stack([q_new, p_new])

particles = np.empty((0, 2))

# Emission
def emit(n):
    q = np.random.uniform(-np.pi, np.pi, size=(n, 1))
    p = np.random.uniform(-2.5, 2.5, size=(n, 1))
    return np.hstack([q, p])

# Color
def energy_color(z):
    H = 0.5 * z[:, 1]**2 + (1 - np.cos(z[:, 0]))
    H = np.clip(H, 0, 3)
    H = H / 3.0
    return plt.cm.inferno(H)

# Figure setup
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-np.pi, np.pi)
ax.set_ylim(-3, 3)
ax.set_aspect('equal')
ax.axis('off')
scat = ax.scatter([], [], s=4)

# Update function
def update(frame):
    global particles

    particles = np.vstack([particles, emit(40)])
    particles = step(particles, 0.04)

    colors = energy_color(particles)

    scat.set_offsets(particles)
    scat.set_facecolors(colors)

    return scat,

ani = FuncAnimation(fig, update, interval=30)
plt.show()
