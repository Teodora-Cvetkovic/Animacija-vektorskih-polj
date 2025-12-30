import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Hamiltonian vector field
def F(z):
    q, p = z[:, 0], z[:, 1]
    dq = p
    dp = -q
    return np.column_stack([dq, dp])

# RK4 step
def rk4_step(z, dt):
    k1 = F(z)
    k2 = F(z + dt/2 * k1)
    k3 = F(z + dt/2 * k2)
    k4 = F(z + dt * k3)
    return z + dt/6 * (k1 + 2*k2 + 2*k3 + k4)

# Euler step
def symplectic_euler(z, dt):
    q, p = z[:, 0], z[:, 1]
    p_new = p - dt * q
    q_new = q + dt * p_new
    return np.column_stack([q_new, p_new])

# Parameters
dt = 0.05
emit_per_frame = 120
max_particles = 12000
domain = 4.5
max_age = 20.0

# Particles storage
particles_rk4 = np.empty((0, 3))
particles_symp = np.empty((0, 3))

# Emission
def emit(n):
    qp = np.random.uniform(
        low=[-2, -2],
        high=[2, 2],
        size=(n, 2)
    )
    age = np.zeros((n, 1))
    return np.hstack([qp, age])

# Figure setup
fig, axes = plt.subplots(1, 2, figsize=(11, 5))

titles = ["RK4 (non-symplectic)", "Symplectic Euler"]
scatters = []

for ax, title in zip(axes, titles):
    ax.set_xlim(-domain, domain)
    ax.set_ylim(-domain, domain)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title)
    scatters.append(
        ax.scatter([], [], s=2, cmap="plasma", vmin=0, vmax=max_age)
    )

# Update function
def update(frame):
    global particles_rk4, particles_symp

    # Emit identical particles
    new = emit(emit_per_frame)
    particles_rk4  = np.vstack([particles_rk4,  new])
    particles_symp = np.vstack([particles_symp, new])

    # Cap size
    if len(particles_rk4) > max_particles:
        particles_rk4  = particles_rk4[-max_particles:]
        particles_symp = particles_symp[-max_particles:]

    # === RK4 ===
    particles_rk4[:, :2] = rk4_step(particles_rk4[:, :2], dt)
    particles_rk4[:, 2] += dt

    # === Symplectic Euler ===
    particles_symp[:, :2] = symplectic_euler(particles_symp[:, :2], dt)
    particles_symp[:, 2] += dt

    # Clip domain
    def clip(P):
        return P[
            (P[:,0] > -domain) & (P[:,0] < domain) &
            (P[:,1] > -domain) & (P[:,1] < domain)
        ]

    particles_rk4  = clip(particles_rk4)
    particles_symp = clip(particles_symp)

    # Draw
    scatters[0].set_offsets(particles_rk4[:, :2])
    scatters[0].set_array(particles_rk4[:, 2])

    scatters[1].set_offsets(particles_symp[:, :2])
    scatters[1].set_array(particles_symp[:, 2])

    return scatters

ani = FuncAnimation(fig, update, interval=30)
plt.show()
