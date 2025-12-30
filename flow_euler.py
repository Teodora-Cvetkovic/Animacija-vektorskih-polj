import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Vector field 
def F(p):
    x, y = p[:, 0], p[:, 1]
    vx = x - x**3
    vy = -y
    return np.column_stack([vx, vy])

# Parameters
dt = 0.01
emit_per_frame = 200
fade = 0.08
domain = 4.5
max_particles = 20000

# Particle storage
particles = np.empty((0, 2))

# Figure setup
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-domain, domain)
ax.set_ylim(-domain, domain)
ax.set_aspect('equal')
ax.axis('off')

scat = ax.scatter([], [], s=1, color='black', alpha=0.9)

# Emission
def emit(n):
    global particles
    new = np.random.uniform(
        low=[-domain, -domain],
        high=[domain, domain],
        size=(n, 2)
    )
    particles = np.vstack([particles, new])

# Update loop
def update(frame):
    global particles

    # Emit new particles
    emit(emit_per_frame)

    # Limit particle count
    if len(particles) > max_particles:
        particles = particles[-max_particles:]

    # Flow step
    v = F(particles)
    particles = particles + dt * v

    # Keep inside domain
    mask = (
        (particles[:, 0] > -domain) &
        (particles[:, 0] < domain) &
        (particles[:, 1] > -domain) &
        (particles[:, 1] < domain)
    )
    particles = particles[mask]

    # Draw
    scat.set_offsets(particles)
    scat.set_alpha(1 - fade)

    return scat,

ani = FuncAnimation(fig, update, interval=30)
plt.show()
