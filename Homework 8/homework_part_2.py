# Eshwary Mishra

import matplotlib.pyplot as plt
import numpy as np

list1 = np.random.randint(0, 201, 50)
list2 = np.random.randint(0, 201, 50)
list3 = np.random.randint(0, 201, 50)

fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Left plot: Line plot for list1 and list2
axs[0].plot(list1, color='blue', linewidth=5, label='List 1')
axs[0].plot(list2, color='green', linestyle=':', label='List 2')
axs[0].set_title('Line Plots of List 1 and List 2')
axs[0].set_xlabel('Index')
axs[0].set_ylabel('Value')
axs[0].legend()

# Right plot: Scatter plot for list3
axs[1].scatter(range(len(list3)), list3, color='purple', marker='^', label='List 3')
axs[1].set_title('Scatter Plot of List 3')
axs[1].set_xlabel('Index')
axs[1].set_ylabel('Value')
axs[1].legend()

plt.tight_layout()
plt.show()
