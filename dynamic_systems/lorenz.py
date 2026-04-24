import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def lorenz(x, y, z, **kwargs):
    s = kwargs.get('s', 10)
    r = kwargs.get('r', 28)
    b = kwargs.get('b', 2.667)

    x_dot = s*(y - x)
    y_dot = r*x - y -x*z
    z_dot = x*y - b*z

    return x_dot, y_dot, z_dot

dt = .01
step_count = 50000

# Need one more for the initial values.
xs = np.empty((step_count+1,))
ys = np.empty((step_count+1,))
zs = np.empty((step_count+1,))

# Function params: `s`, `r`, `b`.
params = np.array([10, 28, 2.667])

# Setting initial values.
xs[0], ys[0], zs[0] = (0., 1., 1.05)

# Stepping through "time".
for i in range(step_count):

    # # Let it grow before introducing disturbances.
    # if i > 100:
    #     if bool(np.random.binomial(1, 0.5, 1)[0]):
    #         index = np.random.binomial(1, 0.5, len(params))
    #         params += index * np.random.randn(len(params))

    # Derivatives of the X, Y, Z state
    x_dot, y_dot, z_dot = lorenz(xs[i], ys[i], zs[i],
                                 s=params[0], r=params[1], b=params[2])
    xs[i+1] = xs[i] + (x_dot * dt)
    ys[i+1] = ys[i] + (y_dot * dt)
    zs[i+1] = zs[i] + (z_dot * dt)

    # print("%.5f; %.5f; %.5f\t\t%.5f; %.5f; %.5f" % (
    #     xs[i+1], ys[i+1], zs[i+1],
    #     params[0], params[1], params[2]
    #     ))

fig = plt.figure()
ax = fig.gca(projection='3d')

ax.plot(xs, ys, zs, lw=0.5)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Lorenz attractor')

plt.show()
