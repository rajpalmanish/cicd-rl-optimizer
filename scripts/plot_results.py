import matplotlib.pyplot as plt
import numpy as np

# simulate reward history
rewards = np.random.normal(-80, 10, 100)

plt.plot(rewards)

plt.title("Training Reward Over Time")
plt.xlabel("Episode")
plt.ylabel("Reward")

plt.show()