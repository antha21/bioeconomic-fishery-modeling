import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# --- 1. Bioeconomic & Financial Parameters ---
c = 150             # Operational cost per unit effort
q = 0.001           # Catchability coefficient
f_avg = 7500        # Average mid-season fish population
X = c / (q * f_avg) # Strike Price (Extraction Cost) = $20.00

days = 90           # Length of the season in days
delta = 0.05 / 365  # Daily risk-free discount rate (Assumed 5% annual)
sigma = 0.03        # Daily market volatility

# --- 2. Create the Grid for Price (p) and Time (t) ---
# Price ranges from $10 to $40
p = np.linspace(10, 40, 100) 
# Time ranges from Day 0 to Day 89.9 (Avoid exactly 90 to prevent divide-by-zero)
t = np.linspace(0, 89.9, 100)  
P, T_mesh = np.meshgrid(p, t)

# Time to maturity (expiration of the season)
tau = days - T_mesh 

# --- 3. The Analytical Black-Scholes Formula ---
d1 = (np.log(P / X) + (delta + 0.5 * sigma**2) * tau) / (sigma * np.sqrt(tau))
d2 = d1 - sigma * np.sqrt(tau)

# Expected discounted profit (Option Value V)
V = P * norm.cdf(d1) - X * np.exp(-delta * tau) * norm.cdf(d2)

# --- 4. 3D Visualization ---
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
surf = ax.plot_surface(P, T_mesh, V, cmap='viridis', edgecolor='none', alpha=0.9)

# Labels and Title
ax.set_xlabel('Market Price p(t) ($)', fontsize=11, labelpad=10)
ax.set_ylabel('Time Elapsed t (Days)', fontsize=11, labelpad=10)
ax.set_zlabel('Expected Profit Value V(p,t) ($)', fontsize=11, labelpad=10)
ax.set_title('Real Options Valuation: Expected Profit Surface of the Fishery', fontsize=14)

# Add a color bar
fig.colorbar(surf, shrink=0.5, aspect=5, label='Option Value V ($)')

# Adjust viewing angle for best presentation
ax.view_init(elev=25, azim=-125)
ax.set_box_aspect(aspect=None, zoom=0.85)
plt.subplots_adjust(left=0.0, right=0.95, top=0.95, bottom=0.0)

# Add extra padding to the layout to prevent clipping
plt.tight_layout(pad=3.0) 
plt.savefig('black_scholes_surface.png', dpi=300, bbox_inches='tight') # bbox_inches forces it to save everything
plt.show()