# integration_spiral.py
# Applies the dream constants to a random bit‑string and measures complexity.

import numpy as np
import matplotlib.pyplot as plt

IRON = 26
BALANCE = 108
MOD = 19
STEPS = 200
LEN = 1140  # 19*60

np.random.seed(42)
bits = np.random.randint(0, 2, LEN)

def apply_iron(b):
    new = b.copy()
    for i in range(len(b)-IRON):
        new[i] = new[i+IRON] = b[i] & b[i+IRON]
    return new

def apply_balance(b):
    cumsum = np.cumsum(np.insert(b, 0, 0))
    smoothed = (cumsum[BALANCE:] - cumsum[:-BALANCE]) / BALANCE
    return (smoothed > 0.5).astype(int)

def apply_modulation(b):
    mask = np.ones(len(b), dtype=bool)
    mask[::MOD] = False
    return b * mask

def complexity(b):
    ones = np.sum(b)
    return abs(len(b) - 2*ones)  # imbalance

history = [complexity(bits)]
for _ in range(STEPS):
    bits = apply_iron(bits)
    bits = apply_balance(bits)
    bits = apply_modulation(bits)
    history.append(complexity(bits))

plt.figure(figsize=(10,5))
plt.plot(history, marker='o', markersize=2)
plt.xlabel('Iteration')
plt.ylabel('Complexity (lower = more integrated)')
plt.title('Integration Spiral')
plt.grid(True)
plt.show()