import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Lorenz vector field
sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0

def F(z):
    x, y, zz = z[:, 0], z[:, 1], z[:, 2]
    dx = sigma * (y - x)
    dy = x * (rho - zz) - y
    dz = x * y - beta * zz
    return np.column_stack([dx, dy, dz])

# RK4
def step(z, dt):
    k1 = F(z)
    k2 = F(z + dt/2 * k1)
    k3 = F(z + dt/2 * k2)
    k4 = F(z + dt * k3)
    return z + dt/6 * (k1 + 2*k2 + 2*k3 + k4)

# Parameters
dt = 0.01

emit_per_frame = 40
max_particles = 6000
max_age = 4.5
particles = np.empty((0, 4))

# Color
def colors_with_fade(particles):
    z = particles[:, 2]
    age = particles[:, 3]

    # Color by height
    z_norm = (z - z.min()) / (z.max() - z.min() + 1e-6)
    colors = plt.cm.plasma(z_norm)

    # Fade by age
    alpha = np.clip(1.0 - age / max_age, 0.0, 1.0)
    colors[:, 3] = alpha

    return colors

# Figure setup
fig, ax = plt.subplots(figsize=(6, 6))

fig.patch.set_facecolor("black")
ax.set_facecolor("black")

ax.set_xlim(-30, 30)
ax.set_ylim(-30, 30)
ax.set_aspect("equal")
ax.axis("off")

scat = ax.scatter([], [], s=1.2, edgecolors="none")


# Emission
def emit(n):
    x = np.random.uniform(-30, 30, (n, 1))
    y = np.random.uniform(-30, 30, (n, 1))
    z = np.random.uniform(0, 50, (n, 1))
    age = np.zeros((n, 1))
    return np.hstack([x, y, z, age])


# Animation
def update(frame):
    global particles

    # Emit new particles
    particles = np.vstack([particles, emit(emit_per_frame)])

    # Advance dynamics
    particles[:, :3] = step(particles[:, :3], dt)
    particles[:, 3] += dt

    # Remove old particles
    particles = particles[particles[:, 3] < max_age]

    # Cap count (safety)
    if len(particles) > max_particles:
        particles = particles[-max_particles:]

    # Draw
    scat.set_offsets(particles[:, :2])
    scat.set_facecolors(colors_with_fade(particles))

    return scat,

ani = FuncAnimation(fig, update, interval=30)
plt.show()
