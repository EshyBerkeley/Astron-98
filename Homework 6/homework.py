import numpy as np
import matplotlib.pyplot as plt

# Problem 1

def sinusoid(x, amp, omega):
    return amp * np.sin(x*omega)

x_data = np.linspace(0, 2 * np.pi, 1000)
amp_data = np.array([4.2, 4, 2, 6, 7])
omega_data = np.array([3.4, 5, 6, 3.3, 1])

plt.figure(figsize=(8, 6))

for A in amp_data:
    for w in omega_data:
        y_data = sinusoid(x_data, A, w)
        plt.plot(x_data, y_data, label=f'A={A}, w={w}')

plt.title("Sinusoidal Functions for Different Amplitudes and Wavelengths")
plt.xlabel("x (radians)")
plt.ylabel("y = A * sin(w * x)")
plt.legend()

plt.grid(True)
plt.show()

# Problem 2

list1 = np.random.randint(0, 101, 40)
list2 = np.random.randint(0, 101, 40)
plt.figure(figsize=(10, 6))
plt.plot(list1, color='orange', linewidth=10, label='List 1 (orange)')
plt.plot(list2, color='red', linestyle='--', label='List 2 (red dashed)')

plt.xlabel('Index')
plt.ylabel('Value')
plt.title('Plot of Two Random Lists')
plt.legend()
plt.grid(True)
plt.show()