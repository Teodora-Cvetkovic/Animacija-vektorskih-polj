import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Vector field
def F(z):
    x, y = z
    return np.array([x - x**3, -y])

# RK4 for solving ODE
def rk4_step(z, h):
    k1 = F(z)
    k2 = F(z + h/2 * k1)
    k3 = F(z + h/2 * k2)
    k4 = F(z + h * k3)
    return z + h/6 * (k1 + 2*k2 + 2*k3 + k4)

# Particle storage
particles_pos = np.empty((0, 2))

# Emit new particles 
def emit_particles(n=5):
    global particles_pos

    # random new particles
    new = np.random.randn(n, 2)
    particles_pos = np.vstack([particles_pos, new])

def keep_particles(z, R=2.5):
    r2 = z[:,0]**2 + z[:,1]**2
    return z[r2 < R**2]

fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.set_title("Flow of a nonlinear ODE")

scatter = ax.scatter([], [], s=15)

dt = 0.05
emit_every = 1   # frames

def update(frame):
    global particles_pos

    # Emit new particles
    if frame % emit_every == 0:
        emit_particles(n=10)

    # Move particles along the flow
    if len(particles_pos) > 0:
        new_pos = np.zeros_like(particles_pos)
        for i, z in enumerate(particles_pos):
            new_pos[i] = rk4_step(z, dt)
        particles_pos = new_pos

    # Remove particles outside domain
    if len(particles_pos) > 0:
        particles_pos = keep_particles(particles_pos)

    # Update plot
    scatter.set_offsets(particles_pos)

    return scatter,

ani = FuncAnimation(fig, update, frames=500, interval=30)
plt.show()
