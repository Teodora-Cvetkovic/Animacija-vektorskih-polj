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
rotation_speed = 0.01   # radians per frame
emit_per_frame = 40
max_particles = 6000
max_age = 4.5
particles = np.empty((0, 4))

# Color
def colors_with_fade_and_depth(particles, depth):
    z = particles[:, 2]
    age = particles[:, 3]

    # Color by height (still meaningful)
    z_norm = (z - z.min()) / (z.max() - z.min() + 1e-6)
    colors = plt.cm.plasma(z_norm)

    # Fade by age
    age_alpha = np.clip(1.0 - age / max_age, 0.0, 1.0)

    # Depth cue: normalize depth
    d = (depth - depth.min()) / (depth.max() - depth.min() + 1e-6)
    depth_alpha = 0.3 + 0.7 * d   # never fully invisible

    colors[:, 3] = age_alpha * depth_alpha
    return colors, depth_alpha

# Projection
def project(particles, theta):
    x, y, z = particles[:, 0], particles[:, 1], particles[:, 2]

    X =  np.cos(theta) * x - np.sin(theta) * y
    Y =  z

    depth = np.sin(theta) * x + np.cos(theta) * y
    return X, Y, depth

# Figure setup
fig, ax = plt.subplots(figsize=(6, 6))

fig.patch.set_facecolor("black")
ax.set_facecolor("black")

ax.set_xlim(-40, 40)
ax.set_ylim(0, 55)
ax.set_aspect("equal")
ax.axis("off")

scat = ax.scatter([], [], s=1.0, edgecolors="none")

# Emission
def emit(n):
    x = np.random.uniform(-30, 30, (n, 1))
    y = np.random.uniform(-30, 30, (n, 1))
    z = np.random.uniform(0, 50, (n, 1))
    age = np.zeros((n, 1))
    return np.hstack([x, y, z, age])


# Animation
theta = 0.0

def update(frame):
    global particles, theta

    # Emit new particles
    particles = np.vstack([particles, emit(emit_per_frame)])

    # Advance dynamics
    particles[:, :3] = step(particles[:, :3], dt)
    particles[:, 3] += dt

    # Remove old particles
    particles = particles[particles[:, 3] < max_age]

    # Cap total count
    if len(particles) > max_particles:
        particles = particles[-max_particles:]

    # Rotate camera
    theta += rotation_speed

    # Project to 2D
    X, Y, depth = project(particles, theta)

    # Color + alpha
    colors, depth_alpha = colors_with_fade_and_depth(particles, depth)

    # Depth → size (subtle but effective)
    sizes = 1.0 + 3.0 * depth_alpha

    # Draw
    scat.set_offsets(np.column_stack([X, Y]))
    scat.set_facecolors(colors)
    scat.set_sizes(sizes)

    return scat,

ani = FuncAnimation(fig, update, interval=30)
plt.show()
