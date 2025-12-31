import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Double gyre velocity field
A = 0.25
eps = 0.25
omega = 2 * np.pi / 10

def velocity(z, t):
    x, y = z[:, 0], z[:, 1]

    a = eps * np.sin(omega * t)
    f = a * x**2 + (1 - 2*a) * x
    df_dx = 2 * a * x + (1 - 2*a)

    u = -np.pi * A * np.sin(np.pi * f) * np.cos(np.pi * y)
    v =  np.pi * A * np.cos(np.pi * f) * np.sin(np.pi * y) * df_dx

    return np.column_stack([u, v])

# RK4
def step(z, t, dt):
    k1 = velocity(z, t)
    k2 = velocity(z + dt/2 * k1, t + dt/2)
    k3 = velocity(z + dt/2 * k2, t + dt/2)
    k4 = velocity(z + dt * k3, t + dt)
    return z + dt/6 * (k1 + 2*k2 + 2*k3 + k4)

# Particle initialization
nx, ny = 120, 60
x = np.linspace(0, 2, nx)
y = np.linspace(0, 1, ny)
X, Y = np.meshgrid(x, y)
particles = np.column_stack([X.ravel(), Y.ravel()])

colors = plt.cm.turbo(particles[:, 0] / 2)

# Figure setup
fig, ax = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor("black")
ax.set_facecolor("black")
ax.set_xlim(0, 2)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.axis("off")
scat = ax.scatter(
    particles[:, 0],
    particles[:, 1],
    s=3,
    facecolors=colors,
    edgecolors="none"
)

# Animation loop
dt = 0.05
t = 0.0

def update(frame):
    global particles, t

    particles = step(particles, t, dt)
    t += dt

    scat.set_offsets(particles)
    return scat,

ani = FuncAnimation(fig, update, interval=30)
plt.show()
