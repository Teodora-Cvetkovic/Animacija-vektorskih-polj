import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Vector field
def F(p):
    x, y = p[:, 0], p[:, 1]
    vx = y
    vy = np.sqrt(np.abs(np.cos(x)))
    return np.column_stack([vx, vy])

# Euler step
def euler_step(p, dt):
    return p + dt * F(p)

# RK4 step
def rk4_step(p, dt):
    k1 = F(p)
    k2 = F(p + dt/2 * k1)
    k3 = F(p + dt/2 * k2)
    k4 = F(p + dt * k3)
    return p + dt/6 * (k1 + 2*k2 + 2*k3 + k4)

# PArameters
dt = 0.01
emit_per_frame = 120
max_particles = 12000
domain = 4.5
fade_alpha = 0.08   # trail fading
max_age = 6.0       # color saturation

# Particle storage
particles_euler = np.empty((0, 3))
particles_rk4   = np.empty((0, 3))

# Emission
def emit(n):
    pos = np.random.uniform(
        low=[-domain, -domain],
        high=[domain, domain],
        size=(n, 2)
    )
    age = np.zeros((n, 1))
    return np.hstack([pos, age])

# Figure setup
fig, axes = plt.subplots(1, 2, figsize=(11, 5))

titles = ["Euler integrator", "RK4 integrator"]
scatters = []

for ax, title in zip(axes, titles):
    ax.set_xlim(-domain, domain)
    ax.set_ylim(-domain, domain)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title)
    scatters.append(ax.scatter([], [], s=2, cmap="plasma", vmin=0, vmax=max_age))

# Update function
def update(frame):
    global particles_euler, particles_rk4

    # Emit identical new particles
    new = emit(emit_per_frame)
    particles_euler = np.vstack([particles_euler, new])
    particles_rk4   = np.vstack([particles_rk4,   new])

    # Cap particle count
    if len(particles_euler) > max_particles:
        particles_euler = particles_euler[-max_particles:]
        particles_rk4   = particles_rk4[-max_particles:]

    # === Euler ===
    particles_euler[:, :2] = euler_step(particles_euler[:, :2], dt)
    particles_euler[:, 2] += dt

    # === RK4 ===
    particles_rk4[:, :2] = rk4_step(particles_rk4[:, :2], dt)
    particles_rk4[:, 2] += dt

    # Remove particles outside domain
    def clip(P):
        return P[
            (P[:,0] > -domain) & (P[:,0] < domain) &
            (P[:,1] > -domain) & (P[:,1] < domain)
        ]

    particles_euler = clip(particles_euler)
    particles_rk4   = clip(particles_rk4)

    # Draw
    scatters[0].set_offsets(particles_euler[:, :2])
    scatters[0].set_array(particles_euler[:, 2])

    scatters[1].set_offsets(particles_rk4[:, :2])
    scatters[1].set_array(particles_rk4[:, 2])

    return scatters

ani = FuncAnimation(fig, update, interval=30)
plt.show()
