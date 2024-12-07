# Eshwary Mishra
# This one was really cool!

import numpy as np
import matplotlib.pyplot as plt

def estimate_pi(N):
    x = np.random.random(N)
    y = np.random.random(N)

    distance = x**2 + y**2
    
    inside_circle = np.count_nonzero(distance <= 1)

    pi_estimate = 4 * inside_circle / N
    return pi_estimate, inside_circle, N

def plot_points(N):
    x = np.random.random(N)
    y = np.random.random(N)

    distance = x**2 + y**2

    # Points inside the quarter circle
    inside_circle_x = x[distance <= 1]
    inside_circle_y = y[distance <= 1]

    # Points outside the quarter circle
    outside_circle_x = x[distance > 1]
    outside_circle_y = y[distance > 1]

    plt.figure(figsize=(6, 6))
    plt.scatter(inside_circle_x, inside_circle_y, color='blue', label='Inside Circle', s=1)
    plt.scatter(outside_circle_x, outside_circle_y, color='red', label='Outside Circle', s=1)
    
    pi_estimate, _, _ = estimate_pi(N)
    plt.title(f'Estimation of π = {pi_estimate:.5f} with N={N}')
    plt.legend(loc='upper right')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.show()

for N in [10, 1000, 100000, 1000000]:
    pi_estimate, _, _ = estimate_pi(N)
    print(f"Estimated π for N={N}: {pi_estimate:.5f}")

plot_points(10000)
